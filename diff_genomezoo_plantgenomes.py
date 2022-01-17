# %% codecell
import json
import pandas as pd
from IPython.display import JSON
# %% codecell
# with open("genomes_angio.json") as read_file:
#     data = json.load(read_file)
# # %% codecell
# order=len(data["children"][0]["children"][0]["children"][0]["children"][0]["children"])
# print(data["children"][0]["children"][0]["children"][0]["children"][0]["children"])
# family=0
# species=[]
# for i in range(0,order):
#     family += len(data["children"][0]["children"][0]["children"][0]["children"][0]["children"][i]["children"])
#
# for i in range(0,family):
#     step = len(data["children"][0]["children"][0]["children"][0]["children"][0]["children"][i]["children"][0]["children"][0]["children"][0]["children"])
# #    print(data["children"][0]["children"][0]["children"][0]["children"][0]["children"][i]["children"][0]["children"][0]["children"][0]["children"])
# #    print(i)
# #    print("step",step)
#     for z in range(0,step):
#         species.append(data["children"][0]["children"][0]["children"][0]["children"][0]["children"][i]["children"][0]["children"][0]["children"][0]["children"][z]["name"])
# print(order)
# print(family)
# print(species)

# %% codecell
# order=len(data["children"][0]["children"][1]["children"])
# print(order)
# #print(data["children"][0]["children"][1]["children"][0]["children"][0]["children"])
# family=0
# species=[]
# for i in range(0,order):
#     #print(family)
#     family += len(data["children"][0]["children"][1]["children"][i])
#     print(data["children"][0]["children"][1]["children"][i]["name"])
# print(family)
# for i in range(0,family):
#     print(data["children"][0]["children"][1]["children"][0]["children"][0]["children"][i]["children"])
#     step = len(data["children"][0]["children"][1]["children"][0]["children"][0]["children"][i]["children"])
#     print(i)
#     print("step",step)
#     for z in range(0,step):
#         species.append(data["children"][0]["children"][1]["children"][0]["children"][0]["children"][i]["children"][0]["children"][0]["children"][0]["children"][z]["name"])
# print(order)
# print(family)
# print(species)

# %% codecell
# with open("genomes_angio.json") as read_file:
#     data = json.load(read_file)
# for (k, v) in data.items():
#     print("Key: " + k)
#     print("Value: " + str(v))
# %% codecell

# %% codecell
with open("genomes_timeline.json") as read_file:
    data = json.load(read_file)
JSON(data)
# %% codecell
#print(data["genomes"][0])
lst = []
for i in data["genomes"]:
    #print(i["ScientificName"] + " " + i["className"])
    lst.append(i["ScientificName"])
print(len(lst))
#print(lst)
# df = pd.DataFrame([list], axis=1)
df = pd.DataFrame(list(zip(lst)), columns=["Eins"])
df
df2 = df.drop_duplicates(subset=["Eins"],keep="first")
df2
# %% codecell
# Webscraping part

# %%codecell

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=3702"
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')
# order = soup.find_all("a", title="order")
# family = soup.find_all("a", title="family")
# kingdom = soup.find_all("a", title="kingdom")
# phylum = soup.find_all("a", title="phylum")
# print(order[0].getText())
# #print(order)
# print(family[0].getText())
# print(kingdom[0].getText())
# print(phylum[0].getText())
# %%codecell


# %%codecell

test = pd.read_csv("names.dmp",sep="|")
#print(test)
test.columns = ["Tax_ID","Name","Drei","Category","Fünf"]
test
test.columns = test.columns.str.strip()
#test
test.replace(r"[\t]","",inplace=True, regex=True)
#test
sel_test = test[test["Category"].str.contains("scientific name")]
sel_test
df

new = pd.merge(sel_test,df,how="inner", on=None, left_on="Name",right_on="Eins", left_index=False, right_index=False, sort=True, copy=True, indicator=False, validate=None)
#new
new.drop(["Drei","Category","Fünf","Eins"], axis=1, inplace=True)
#new
# %%codecell
order_lst = []
family_lst = []
kingdom_lst = []
phylum_lst = []

for index, row in new.iterrows():
    URL = 'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=' + str(row["Tax_ID"])
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    order = soup.find_all("a", title="order")
    family = soup.find_all("a", title="family")
    kingdom = soup.find_all("a", title="kingdom")
    phylum = soup.find_all("a", title="phylum")
    #print(order)
    if not order:
        order_lst.append("")
    else:
        order_lst.append(order[0].getText())
    if not family:
        family_lst.append("")
    else:
        family_lst.append(family[0].getText())
    if not kingdom:
        kingdom_lst.append("")
    else:
        kingdom_lst.append(kingdom[0].getText())
    if not phylum:
        phylum_lst.append("")
    else:
        phylum_lst.append(phylum[0].getText())
#new
new["Order"] = order_lst
new["Family"] = family_lst
new["Kingdom"] = kingdom_lst
new["Phylum"] = phylum_lst
new


for_check = new["Name"]
for_check[1]
temptemp = []
for i in lst:
    if not i in for_check.unique():
        temptemp.append(i)
print(temptemp)
temptempdf = pd.DataFrame({"irgendwas":temptemp})
temptempdf.to_csv("nichterfasst.csv",sep=";")

lst

genomezoo = pd.read_csv("genomezoo.csv",sep=";")
gz_name = genomezoo[["scientific name","scientific name"]]
gz_name.columns = ["scientific name","egal"]

final = pd.merge(gz_name,new,how="inner", on=None, left_on="scientific name",right_on="Name", left_index=False, right_index=False, sort=True, copy=True, indicator=False, validate=None)
#new2 = pd.merge(gz_name,new,how="inner", on=None, left_on="scientific name",right_on="Name", left_index=False, right_index=False, sort=True, copy=True, indicator=False, validate=None).query('_merge == "right_only"').drop('_merge', 1)

test2 = (gz_name.merge(new, on=None,left_on="scientific name",right_on="Name", how='right', indicator=True).query('_merge == "right_only"').drop('_merge', 1))
final
test2
final.to_csv("difference.csv",sep=";")
test2.to_csv("final.csv",sep=";")
#print(order_lst)
# %%codecell
#"1\t"

#"\tall\t"
