## https://www.archchinese.com/chinese_english_dictionary.html?find=
# https://hanzicraft.com/character/
from selenium import webdriver
from db import insert_list, insert, raw, select, update
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
from utils import cn_re, idc_re, decompose, disambiguate_radical, config
from sources.sources import sources

def fill():
  config_params = config("database.ini", "sources")
  driver = webdriver.Chrome(ChromeDriverManager().install())
  
  for src in sources:
    src_type = src["type"]
    path = src["path"]
    source_key = src["source_key"]
    
    source_url = config_params[source_key]

    if src_type == "series":
      driver.get(source_url + "/" + path)
      
      content = driver.page_source
      soup = BeautifulSoup(content)
      vols_links = soup.select(".acin a")
      
      vol_num = 1
      
      for vol_link in vols_links:
        driver.get(vol_link.attrs["href"])
        vol_content = driver.page_source
        vol_soup = BeautifulSoup(vol_content)
        chapter_links = vol_soup.select(".book-list a")
        
        ch_num = 1
        
        for chapter_link in chapter_links:
          chapter_title = chapter_link.attrs["title"]
          driver.get(chapter_link.attrs["href"])
          chapter_content = driver.page_source
          chapter_soup = BeautifulSoup(chapter_content)
          chapter_text_block = chapter_soup.select("#nr1")
          paras = chapter_text_block[0].select("p") if chapter_text_block else []
          
          para_num = 1
          
          for para in paras:
            text = para.text
            # Ignore rubbish text
            is_garbage = "m e n g R u a n" in text
            if not is_garbage:
              print(text)
              para_num += 1
          
          ch_num += 1
        
      vol_num += 1
    
  
  

        
fill()



