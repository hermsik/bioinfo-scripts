######################
### RAW SCRIPT FOR SCIENTIFIC NAME COMPARISON
######################

# Looks for an updated scientific name based on taxID from NCBI

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

gz = pd.read_csv("genomezoo_17-12-20-temp.csv", sep="{")

# print(gz["taxID from NCBI"])

for index, row in gz.iterrows(): # Iterate over .csv table
    # print(row["taxID from NCBI"], row["scientific name"])
    URL = 'https://www.ncbi.nlm.nih.gov/taxonomy/?term=' + str(row["taxID from NCBI"]) # NCBI website link with dynamic taxID input
    #URL = 'https://www.ncbi.nlm.nih.gov/taxonomy/?term=148305'
    page = requests.get(URL) # Open Website
    soup = BeautifulSoup(page.content, 'html.parser') # Parse Website with BS4
    #print(soup)
    names = soup.select('.title') # Select HTML with class="title"
    #print(name)
    #print(names)
    name = names[0].getText() # Select inner HTML text of object
    # print(name)
    # print(row["taxID from NCBI"])
    if str(name) != str(row["scientific name"]): # Check if online name is not equal to table name
        print(name + "\t" + str(row["taxID from NCBI"]))

    # test = soup.find_all("p",class_="title")
    # print(test)
    # for t in test:
    #     link = t.find('a').get_text()
    #     #print(link)

    # print("OK, now wait")
    # time.sleep(1)
        #print(link)
#results = soup.find(id="maincontent")
#print(results)
#link = results.find_all('a')['href']
#<a href="/Taxonomy/Browser/wwwtax.cgi?id=148305" ref="ncbi_uid=148305&amp;link_uid=148305&amp;ordinalpos=1">Pyricularia grisea</a>
# name = results.find_all('div',class_='rprt')
# for result in results:
#     link = name.find('a'['href'])
#print(link)
#print(results.prettify())
#name = soup.find_all('div', class_='title')
#print(name)
    #taxName = soup.find_all("h2",string="")
    # if taxName[0].text != row["taxID from NCBI"]:
    #     print(taxName[0].text)
    # print("OK, now wait")
    # time.sleep(5)
