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
      
      # Book description
      bk_attrs_dict = {}
      
      book_describe = soup.select(".book-describe")
      bk_title_el = book_describe[0].select("h1") if book_describe else None
      bk_title = bk_title_el[0].text if bk_title_el else None
      bk_attrs_dict["title"] = bk_title
      
      bk_attrs = soup.select(".book-describe > p")
      
      for bk_attr in bk_attrs:
        if bk_attr and bk_attr.text:
          bk_attr_txt = bk_attr.text
          bk_attr_arr = bk_attr_txt.split("：")
          value_key = None
          if "作者" in bk_attr_txt:
            value_key = "author"
          elif "类型" in bk_attr_txt:
            value_key = "genre"
          
          lan = None
          if "[" in bk_attr_txt and "]" in bk_attr_txt:
            lan_prep = re.search(r"\[(\w+)\]", bk_attr_txt)
            lan = lan_prep.group(1) if lan_prep else None
            bk_attrs_dict["source_language"] = lan
          
          if value_key:
            bk_attrs_dict[value_key] = bk_attr_arr[1] if len(bk_attr_arr) > 1 else None
          
      # Save book attributes
      # - Check sentences
      db_bk = select("books", ["id", "title"], "title = %s", (bk_title,))
      db_bk = db_bk[0] if db_bk else None
      # - Insert book
      if not db_bk:
        db_bk = insert("books", bk_attrs_dict)
          
      vols_links = soup.select(".acin a")
      
      vol_num = 1
      
      # Volume
      for vol_link in vols_links:
        driver.get(vol_link.attrs["href"])
        vol_content = driver.page_source
        vol_soup = BeautifulSoup(vol_content)
        chapter_links = vol_soup.select(".book-list a")
        
        ch_num = 1
        
        # Chapter
        for chapter_link in tqdm(chapter_links):
          chapter_title = chapter_link.attrs["title"]
          ch_href = chapter_link.attrs["href"]
          driver.get(ch_href)
          chapter_content = driver.page_source
          chapter_soup = BeautifulSoup(chapter_content)
          
          subchapter_navi_el = chapter_soup.select(".apnavi")
          subchapters = subchapter_navi_el[0].select("a") if subchapter_navi_el else [None]
          
          subch_num = 1
          
          # Sub-chapter
          for subchapter in subchapters:
            sc_href = subchapter.attrs["href"] if subchapter else ch_href
            driver.get(sc_href)
            subchapter_content = driver.page_source
            subchapter_soup = BeautifulSoup(subchapter_content)
            subchapter_text_block = subchapter_soup.select("#nr1")
            paras = subchapter_text_block[0].select("p") if subchapter_text_block else []
          
            para_num = 1
            
            # Paragraph
            for para in paras:
              text = para.text
              
              if text:
                # Ignore rubbish text
                text_remove_format = text.replace(" ", "").upper()
                is_garbage = "MENGRUAN" in text_remove_format
                if not is_garbage:
                  # Check if text exists
                  snt = select("sentences", ["id"], "book_id = %s and text = %s and paragraph_num = %s and chapter_num = %s and subchapter_num = %s and volume_num = %s", (db_bk[0], text, para_num, ch_num, subch_num, vol_num))
                  snt = snt[0] if snt else None
                  # Save text
                  if not snt:
                    stc_save = insert("sentences", {
                      "text": text,
                      "book_id": db_bk[0],
                      "paragraph_num": para_num,
                      "chapter_num": ch_num,
                      "subchapter_num": subch_num,
                      "volume_num": vol_num
                    })
                  para_num += 1
                  
            subch_num += 1
          
          ch_num += 1
        
      vol_num += 1
    
  
  

        
fill()



