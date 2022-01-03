## https://www.archchinese.com/chinese_english_dictionary.html?find=
# https://hanzicraft.com/character/
from selenium import webdriver
from db import insert_list, insert, raw, select, update
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
from utils import cn_re, idc_re, decompose, disambiguate_radical


def dictionary_fill():
  char_cols = ["id", "character", "variant", "traditional_id", "formation", "composition"]
  characters_db = select("characters", char_cols, " radical IS NULL OR (sound_component IS NULL AND meaning_component IS NULL)")
  characters = pd.DataFrame(data=characters_db, columns=char_cols)
  
  driver = webdriver.Chrome(ChromeDriverManager().install())

  
  for index, char_row in tqdm(characters.iterrows(), total=characters.shape[0]):
    id, character, variant, traditional_id, formation, composition = char_row
    driver.get("https://www.archchinese.com/chinese_english_dictionary.html?find=" + character)
    content = driver.page_source
    soup = BeautifulSoup(content)
    char_def = soup.select('#charDef')

    if char_def and char_def[0].children:
      radical_text = None
      component_text = None
      form_text = None
      for a in char_def[0].children:
        if hasattr(a, 'get_text'):
          a_text = a.get_text().strip('\n')
          
          if "Radical" in a_text:
            radical = a.nextSibling
            radical_text = radical.get_text().strip('\n') if hasattr(radical, 'get_text') else None
          elif "Component" in a_text:
            component = a.nextSibling
            component_text = component.get_text().strip('\n') if hasattr(component, 'get_text') else None
          elif "Formation" in a_text:
            form = a.nextSibling
            form_text = form.get_text().strip('\n') if hasattr(form, 'get_text') else None
            # Pictophonetic
      if radical_text or component_text or form_text:
        # print(radical_text, component_text, form_text)
        update_cols = None
        update_col_vals = None
        if form_text == "Ideograph" or form_text == "Pictograph":
          update_cols = ["radical", "meaning_component"]
          update_col_vals = (radical_text, component_text)
        elif form_text == "Pictophonetic":
          update_cols = ["radical", "sound_component"]
          update_col_vals = (radical_text, component_text)
        
        if update_cols and update_col_vals:
          update("characters", update_cols, update_col_vals, "id = %s" % (id,))
          
def fill_radicals():
  char_cols = ["id", "character", "variant", "traditional_id", "formation", "composition", "radical", "radical_id"]
  characters_db = select("characters", char_cols, " radical_id IS NULL AND radical IS NOT NULL")
  characters = pd.DataFrame(data=characters_db, columns=char_cols)
  rad_cols = ["id", "simplified", "traditional", "variants", "kangxi"]
  
  # Iterate each character
  for index, char_row in tqdm(characters.iterrows(), total=characters.shape[0]):
    id, character, variant, traditional_id, formation, composition, radical, radical_id = char_row
    # Find character's radical
    radicals = pd.DataFrame(data=select("radicals", rad_cols, "simplified = %s OR traditional = %s", (radical,radical)), columns=rad_cols)
    radical_id = None
    if len(radicals) == 1:
      # Assign radical ID
      radical_id = radicals.iloc[0]["id"]
    else:
      # If ambiguous radical
      # For simplified, use traditional
      if variant == 's':
        trad_chars = select("characters", char_cols, " id = %s" % (traditional_id,))
        trad_char = trad_chars[0] if trad_chars and len(trad_chars) > 0 else None
        trad_char_rad_id = trad_char[7] if trad_char else None
        if trad_char and trad_char_rad_id:
          # Assign traditional character's radical id
          radical_id = trad_char_rad_id
    
    if not radical_id:
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
          # Filter only composition list for sound component
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
              # Assign radical ID
              radical_id = row["id"]
            elif len(matches) > 1:
              rad_id = disambiguate_radical(chars_only, matches)
              if rad_id:
                match_filtered = next(filter(lambda x : x["row"]["id"] == rad_id, matches))
                match = match_filtered["match"] if match_filtered else None
                if match:
                  # Assign radical ID
                  radical_id = rad_id
              else:
                # Filter out only the outer-most matches
                matches_out = radical_outer_check(matches, composition)
                if matches_out:
                  # If multiple unresolved radicals, prefer the higher Kangxi value
                  max_kx = max(matches_out, key=lambda x : x["row"]["kangxi"])
                  match_filtered = next(filter(lambda x : x["row"]["id"] == max_kx["row"]["id"], matches_out)) if max_kx else None
                  match = match_filtered["match"] if match_filtered else None
                  if match:
                    # Assign radical ID
                    radical_id = rad_id
    if radical_id:
      update("characters", ["radical_id"], (radical_id,), "id = %s" % (id,))
    

        
# dictionary_fill()
fill_radicals()



