from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from db import insert_list, insert, raw, select, update
from bs4 import BeautifulSoup
import pandas as pd
import re
from utils import cn_re, idc_re, decompose, disambiguate_radical
import json

def parse_radicals():
  htmls = [
    {
      "type": "traditional",
      "html": "traditional_chinese_radicals.html"
    },
    {
      "type": "simplified",
      "html": "arch_chinese_radicals.html"
    }
  ]

  driver = webdriver.Chrome(ChromeDriverManager().install())
  # driver = webdriver.Chrome("/usr/local/bin/chromedriver")
  radicals = {}

  for html in htmls:
    driver.get(
        "https://www.archchinese.com/" + html["html"])

    content = driver.page_source
    soup = BeautifulSoup(content)

    print("Parsing html page . . .")

    for a in soup.select('.table-responsive > .table.table-condensed.table-striped > tbody > tr'):
      res = {}
      cells = a.select('td')
      if html["type"] == "traditional":
        if cells[0].has_attr("class") and cells[0]['class'][0] == "english":
          res["traditional"] = cells[1].get_text().strip('\n')
          # res["traditional"] = cells[5].get_text().strip("()") or res["simplified"]
          res["english"] = cells[2].get_text().strip('\n')
          res["pinyin"] = cells[3].get_text().strip('\n')
          res["strokes_traditional"] = cells[4].get_text()
          num = cells[0].get_text()
          res["id"] = num
          res["kangxi"] = num
          
          variants = cells[5].select('a')
          if len(variants) > 0:
            var_list = list(filter((lambda x: x and '(' not in x), list(map((lambda x: x.get_text().strip()), variants))))
            if len(var_list) > 0:
              res["variants"] = ','.join(var_list)
          
          radicals[num] = res
      else:
        if cells[0].has_attr("class") and cells[0]['class'][0] == "english":        
          res["simplified"] = cells[1].get_text().strip('\n')
          res["strokes"] = cells[4].get_text()
          num = cells[0].get_text()
          radicals[num]["simplified"] = res["simplified"]
          radicals[num]["strokes_simplified"] = res["strokes"]
          
  print("Parsing radicals complete")

  for i in radicals:
    insert("radicals", radicals[i])
    
  
def radical_outer_check(matches, composition):
  decomp = decompose(composition)
  match_res = []
  if decomp and matches:
    for match in matches:
      rad_str = match["match"][0]
      out_match = list(filter(lambda child : child == rad_str, decomp["children"]))
      if out_match:
        match_res.append(match)
  return match_res

def assign_radical(character_id, formation_type, base_component, radical, radical_id):
  cols = ["sound_component", "meaning_component", "radical", "radical_id"] if formation_type == 'sound_meaning' else ["sound_component", "radical", "radical_id"]
  col_vals = (base_component, base_component, radical, radical_id) if formation_type == 'sound_meaning' else (base_component, radical, radical_id)
  update("characters", cols, col_vals, "id = %s" % (character_id,))

def match_radicals():
  # Radicals
  rad_cols = ["id", "simplified", "traditional", "variants", "kangxi"]
  radicals = pd.DataFrame(data=select("radicals", rad_cols, ""), columns=rad_cols)
  # - Radical variants
  radicals["variants"] = radicals["variants"].apply(lambda variant : [x.strip() for x in variant.split(',')] if variant else None)
  
  # Characters
  char_cols = ["id", "character", "variant", "traditional_id", "formation", "composition"]
  characters = pd.DataFrame(data=select("characters", char_cols, ""), columns=char_cols)
  
  for index, char_row in tqdm(characters.iterrows(), total=characters.shape[0]):
    id, character, variant, traditional_id, formation, composition = char_row
    if composition and formation:
      chars_only = re.findall(cn_re, composition)
      formation_type = None
      if re.findall(r'^.+亦聲$', formation):
        formation_type = 'sound_meaning'
      if formation_type != 'sound_meaning' and re.findall(r'聲$', formation):
        formation_type = 'sound'
      
      if formation_type == 'sound_meaning' or formation_type == 'sound':
        # Phonetic
        replace_char = '亦聲' if formation_type == 'sound_meaning' else '聲'
        sound_comp = formation.replace(replace_char, '')
        search_list = list(filter((lambda ch : ch != sound_comp), chars_only)) if chars_only and len(chars_only) > 0 else None

        if search_list and len(search_list) > 0:
          search_concat = "[%s]" % (''.join(search_list),)
          search_reg = re.compile(search_concat)
          
          # Find matching radical
          matches = []
          for index, rad_row in radicals.iterrows():
            match = None
            rad_traditional = rad_row["traditional"]
            match = re.findall(search_reg, rad_traditional)
            
            if not match:
              rad_simplified = rad_row["simplified"]
              match = re.findall(search_reg, rad_simplified)
            
            if not match:
              rad_variants = rad_row["variants"]
              if rad_variants and len(rad_variants) > 0:
                for rad_variant in rad_variants:
                  match = re.findall(search_reg, rad_variant)
            
            if match:
              matches.append({ "row": rad_row, "match": match })
          # By right, there should be only one match per character
          if len(matches) == 1:
            row = matches[0]["row"]
            match = matches[0]["match"]
            assign_radical(id, formation_type, sound_comp, match[0], row["id"])
          elif len(matches) > 1:
            rad_id = disambiguate_radical(chars_only, matches)
            if rad_id:
              match_filtered = next(filter(lambda x : x["row"]["id"] == rad_id, matches))
              match = match_filtered["match"] if match_filtered else None
              if match:
                assign_radical(id, formation_type, sound_comp, match[0], rad_id)
            else:
              # Filter out only the outer-most matches
              matches_out = radical_outer_check(matches, composition)
              if matches_out:
                # If multiple unresolved radicals, prefer the higher Kangxi value
                max_kx = max(matches_out, key=lambda x : x["row"]["kangxi"])
                match_filtered = next(filter(lambda x : x["row"]["id"] == max_kx["row"]["id"], matches_out)) if max_kx else None
                match = match_filtered["match"] if match_filtered else None
                if match:
                  assign_radical(id, formation_type, sound_comp, match[0], rad_id)

parse_radicals()
match_radicals()





