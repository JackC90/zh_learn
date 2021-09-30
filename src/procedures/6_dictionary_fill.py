## https://www.archchinese.com/chinese_english_dictionary.html?find=
# https://hanzicraft.com/character/
from selenium import webdriver
from db import insert_list, insert, raw, select, update
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re


def difctionary_fill():
  char_cols = ["id", "character", "variant", "traditional_id", "formation", "composition"]
  characters = select("characters", char_cols, "sound_component IS NULL and meaning_component IS NULL")
  characters = pd.DataFrame(data=select("characters", char_cols, ""), columns=char_cols)
  
  driver = webdriver.Chrome(ChromeDriverManager().install())

  
  for index, char_row in tqdm(characters.iterrows(), total=characters.shape[0]):
    id, character, variant, traditional_id, formation, composition = char_row
    driver.get("https://www.archchinese.com/chinese_english_dictionary.html?find=" + character)
    content = driver.page_source
    soup = BeautifulSoup(content)

    for a in soup.select('#charDef').children:
      a_text = a.get_text().strip('\n')
      if "Radical" in a_text:
        radical = a.nextSibling
        radical_text = radical.get_text().strip('\n')
      elif "Component" in a_text:
        component = a.nextSibling
        component_text = component.get_text().strip('\n')
      elif "Formation" in a_text:
        formation = a.nextSibling
        formation_text = formation.get_text().strip('\n')
        # Pictophonetic
        