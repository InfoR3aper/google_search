# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 14:52:16 2019

@author: preya
"""

#importing the modules
from selenium import webdriver
from bs4  import BeautifulSoup

#opening chrome

#hint: If your browser is having proxy configuration required
openbrouser=True
#exe path of chrome link to download https://chromedriver.chromium.org/downloads
exe_path="C:\your\path\chromedriver.exe"
if(openbrouser):
    driver = webdriver.Chrome(exe_path)
else:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)

#input
word = input("Search for a word: ")

#organizing input to pass in link
search = word.replace(' ','+')
link = "https://www.google.com/search?q="+search+"+meaning"+"&safe=active"
driver.get(link)

#declaring the required variable
content = driver.page_source
soup = BeautifulSoup(content)
synonyms=[]
antonyms=[]
example_of_noun=[]
example_of_adjective=[]
meaning=""
searchme=[]
other_website_content=""
what_is_search=""

#what is "word" search with keyword "what is "
temp_word_list=list(word.split(' '))
if(temp_word_list[0]=="what"):
    searchme=soup.findAll('div', {'class':'SALvLe farUxc mJ2Mod'})
    for i in searchme:
        sub_searchme=i.find("span")
        try:
            what_is_search=str(sub_searchme).split("<span>")[1].split('<')[0]
        except:
            what_is_search=str(sub_searchme)

#to search other website content
other_website_contents=soup.findAll('span', {'class':'ILfuVd c3biWd'})
for i in other_website_contents:
    other_website_content=str(i.find("span"))

#for searching adjective and noun
#noun
containers = soup.findAll('div', {'class':'lr_container mod yc7KLc'})            
for i in containers:
    nounOrAdjective = i.findAll('div', {'class':'lr_dct_sf_h oylZkd'})
    for j in nounOrAdjective:
        if(j.text=='noun'):
            noun = i.find('div', {'class':'lr_dct_sf_sen Uekwlc XpoqFe'}).text
            noun_split = noun.split('"')
            for i in range(len(noun_split)):
                if(i==0):
                    meaning=noun_split[i]
                elif 'synonyms' in str(noun_split[i]):
                    synonyms.append(noun_split[i])
                elif 'antonyms' in str(noun_split[i]):
                    antonyms.append(noun_split[i])
                else:
                    example_of_noun.append(noun_split[i])
#adjective 
for i in containers:
    nounOrAdjective = i.findAll('div', {'class':'lr_dct_sf_h oylZkd'})
    for j in nounOrAdjective:
        if(j.text=='adjective'):
            adjective = i.find('div', {'class':'lr_dct_sf_sen Uekwlc XpoqFe'}).text
            adjective_split = adjective.split('"')
            for i in range(len(adjective_split)):
                if(i==0 & len(meaning)==0):
                    meaning=adjective_split[i]
                elif 'synonyms' in str(adjective_split[i]):
                    synonyms.append(adjective_split[i])
                elif 'antonyms' in str(adjective_split[i]):
                    antonyms.append(adjective_split[i])
                else:
                    example_of_adjective.append(adjective_split[i])

#printme method defined
def printme(x, listname):
    if(len(x)>0):
        print("\n\nList of " + listname+"")
        for i in range(len(x)):
            if(len(x[i])>20):
                print(str(i+1)+" "+x[i]+"\n")

#final output code goes here
if(len(meaning)>0 or len(searchme)>0 or len(other_website_content)>0):  
    if(len(other_website_content)>0):
        print(word+" : "+other_website_content)    
    if(len(meaning)>0):
        try:
            meaning=meaning.split('1')[1].split('.')[1].split()
            meaning=" ".join(meaning)
            print(word+" Meaning :"+meaning)
        except:
            print(word+" Meaning :"+meaning)
    if(len(what_is_search)>0):
        print(word+" : "+what_is_search)
    printme(example_of_noun, "Examples of Noun")
    printme(example_of_adjective, "Examples of Adjective")
    printme(synonyms, "Synonyms")
    printme(antonyms, "Antonyms")
else:
    print("you have entered wrong spealing of word,\nPlease Google the correct spealing!")