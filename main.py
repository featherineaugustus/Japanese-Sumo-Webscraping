# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 22:02:38 2022

https://medium.com/analytics-vidhya/web-scraping-a-wikipedia-table-into-a-dataframe-c52617e1f451
@author: Featherine
"""

import os
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import matplotlib.pyplot as plt
from collections import Counter
from pprint import pprint
import matplotlib.font_manager as fm
from wordcloud import WordCloud



path_font = 'Noto_Serif_JP/NotoSerifJP-Bold.otf'
fprop = fm.FontProperties(fname=path_font)

plt.close('all')


if not os.path.exists('Results'):
    os.makedirs('Results')

#%%############################################################################
# get the response in the form of html
wikiurl="https://en.wikipedia.org/wiki/List_of_yokozuna"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
#print(response.status_code)

# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')
indiatable=soup.find('table',{'class':"wikitable"})

#%%############################################################################

df = pd.read_html(str(indiatable))
# convert list to dataframe
df = pd.DataFrame(df[0])

df = df.rename(columns={'Promoted[2]': 'Promoted',
                        'Elder name[3]': 'Elder name',
                        '(in Japanese)': 'Name J'})

df[['First Name', 'Last Name']] = df['Name'].str.split(' ', 1, expand=True)
df[['First Name J', 'Last Name J']] = df['Name J'].str.split(' ', 1, expand=True)

#%%############################################################################
df_10 = df.sort_values('Top DivisionChampionships')
df_10 = df_10[df_10['Top DivisionChampionships']>=10]

y = list(range(len(df_10)))
yticks = list(df_10['First Name J'])
df_10['Index'] = y

df_10.plot.barh(x='First Name J', y='Top DivisionChampionships', figsize=(12,6))
plt.title('Yokozuna with at least 10 Top Division Championships')
plt.xlabel('Number of Top Division Championships')
plt.ylabel('Yokozuna')
plt.yticks(y, yticks, fontproperties=fprop, fontsize=12, rotation=0)
plt.show()
plt.savefig('Results/Most Wins.png')
plt.close('all')

#%%############################################################################
unique_char = ''.join(df['First Name J'].to_list())

text = unique_char
text = ' '.join([*text])

#pprint(Counter(unique_char))
unique_char = dict(Counter(unique_char))

unique_char = sorted(unique_char.items(), key=lambda x: x[1], reverse=True)

unique_char_keys = []
unique_char_values = []

for item in unique_char:
    if item[1] > 2:
        unique_char_keys.append(item[0])
        unique_char_values.append(item[1])

x = list(range(len(unique_char_values)))
y = unique_char_values
xticks = unique_char_keys

# creating the bar plot
plt.figure(figsize=(8, 4))
plt.bar(x, y, color ='maroon',
        width = 0.4)

plt.xticks(x, xticks, fontproperties=fprop, fontsize=12, rotation=0)
 
plt.xlabel('Characters')
plt.ylabel('Count')
plt.title('Most popular characters in the first name of Yokozuna')
plt.show()
plt.savefig('Results/First Name Bar.png')
plt.close('all')

#%%############################################################################
wordcloud = WordCloud(background_color="white", font_path=path_font,
                      width=900, height=500).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.title('Word Cloud')
plt.axis("off")
plt.show()
plt.savefig('Results/First Name Word Cloud.png')
plt.close('all')

#%%############################################################################

#%%############################################################################