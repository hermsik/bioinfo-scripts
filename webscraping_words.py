from bs4 import BeautifulSoup
from time import sleep
from random import randint
import requests
import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("website")
parser.add_argument("output")
parser.add_argument('subpage', nargs='+')
args = parser.parse_args()

main_url = args.website
sub_urls = args.subpage
url_found = []

for sub in sub_urls:
    page = requests.get(main_url + str(sub))
    soup = BeautifulSoup(page.text,"html.parser")
    found_strings = soup.find_all(string=re.compile("Physcomitrella"))
    sleep(randint(2,10)) ###################### IMPORTANT CHECK FOR REAL WEBSITES!!
    url_found.append(found_strings)

df = pd.DataFrame()
for i,z in enumerate(sub_urls):
    df1 = pd.DataFrame({str(z):url_found[i]})
    df = pd.concat([df,df1],axis=1)

df.to_csv(args.output + ".csv")
