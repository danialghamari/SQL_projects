'''
    Creating a list of names
    The initial intent was to gather the data from https://1000randomnames.com/ website.
    But since it uses JS to generate the names everytime it loads, I simply obtain the list of (lastnames, boy_firstnames,
    girl_firstnames), and then use my own script to generate the final data.
    Given the premise of "real names", I have allowed for ducplicate names to exist (same was adopted in the website script).
'''

from bs4 import BeautifulSoup as bs
from operator import itemgetter
from itertools import product
import requests as req, os, re, random, time

## Get the path of this file
cur_dir = os.path.dirname(os.path.realpath(__file__))


## Get the JS script that generates the names in the webpage
html_page = req.get('https://1000randomnames.com/')
bs_obj = bs(html_page.text , 'html.parser')

scripts = bs_obj.find_all("script")

for script in scripts:
    if 'lastNames' in script.text:
        names_script = script.text
        break

## Get the list of "last,boy_first,girl_first" names

lastnames_str = re.search(r'lastNames = \[(.*?)\]', names_script, re.DOTALL).group(0)
lastnames_list = re.findall(r'\"([^"]*)\"',lastnames_str)

boy_firstnames_str = re.search(r'maleFirstNames = \[(.*?)\]', names_script, re.DOTALL).group(0)
boy_firstnames_list = re.findall(r'\"([^"]*)\"',boy_firstnames_str)

girl_firstnames_str = re.search(r'femaleFirstNames = \[(.*?)\]', names_script, re.DOTALL).group(0)
girl_firstnames_list = re.findall(r'\"([^"]*)\"',girl_firstnames_str)


## Generate index for 1-million male and female names
index_names = list(product(range(len(boy_firstnames_list)),
                 range(len(lastnames_list))))
## Randomly generate 10000 names index
random_index_boys = random.choices(index_names,  k = 1000)
random_index_girls = random.choices(index_names,  k = 1000)

male_names = [boy_firstnames_list[i[0]]+' '+lastnames_list[i[1]] for i in random_index_boys]
female_names = [girl_firstnames_list[i[0]]+' '+lastnames_list[i[1]] for i in random_index_girls]

with open(os.path.join(cur_dir,"..","Data",'name.csv'),'w') as file:
    file.write('id, names\n')
    for idx in range(len(male_names)):
        file.write(f'{idx*2+1}, {male_names[idx]}\n')
        file.write(f'{idx*2+2}, {female_names[idx]}\n')
