from turtle import clear
import requests
from bs4 import BeautifulSoup
import re
import spacy
import pandas as pd
from heapq import heapify, heappush, heappushpop, nlargest

#1. Get all the OCC 1990 codes
occ_codes_1990 = []
html_doc = requests.get('https://usa.ipums.org/usa/volii/occ1990.shtml').content
soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.findAll('table')[1] # This is the table element where all the codes are stored
rows = table.findAll('tr')
for row in rows:
    # Rows with valid OCC codes only have two td elements.
    tds = row.find_all('td')
    if (len(tds) != 2):
        continue
    # OCC 1990 codes are exactly three-digits
    code = tds[0].text.strip()
    if (len(code) != 3 or not bool(re.match('\d\d\d',code))):
        continue
    # Get code label
    label = tds[1].text
    # Store this code & label pair
    occ_codes_1990.append((code,label))


class MaxHeap():
    def __init__(self, top_n):
        self.h = []
        self.length = top_n
        heapify(self.h)
        
    def add(self, element):
        if len(self.h) < self.length:
            heappush(self.h, element)
        else:
            heappushpop(self.h, element)
            
    def getTop(self):
        return nlargest(self.length, self.h)

#2. Matching function
# Given a OCC 2002 code
# Print the best match in OCC 1990
nlp = spacy.load("en_core_web_md") # Use this command to download this: python -m spacy download en_core_web_md
def match(code2002, label2002):
    # Basically, loop over all OCC 1990 codes and see which one is the most similar
    nlp_label_2002 = nlp(label2002)
    five_possible_matches = MaxHeap(5)
    for tup in occ_codes_1990:
        nlp_label_1990 = nlp(tup[1])
        similarity = nlp_label_2002.similarity(nlp_label_1990)
        five_possible_matches.add((similarity,tup[0], tup[1]))
        if (similarity > 0.99):
            break
    return five_possible_matches

#3. Get the OCC 2002 codes that we want to match to OCC 1990
df = pd.read_excel("./acs_nlsy79_occ_crosswalk.xlsx", engine="openpyxl")
with open("test.txt", "w") as myfile:
    for index, row in df.iterrows():
        if (index < 512 or index > 550): # Freddie only looks at the 300+ rows
            continue
        try:
            print(str(index) + ", matching code: " + str(row[0]) + "(" + str(row[1]) + ")\n")
            matches = match(str(row[0]), str(row[1]))
        except:
            print("Skipping an empty row: " + str(index))
        result = "--------------\n"
        result += "Potential matches for 2002 code: " + str(row[0]) + "(" + str(row[1]) + ")\n"
        for m in matches.getTop():
            result += str(m[0]) +", " + m[1] +  "(" + m[2] + ")\n"
        result += "\n"
        myfile.write(result)