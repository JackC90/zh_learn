from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from db import insert_list, insert, raw, select, update
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

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

    
  



