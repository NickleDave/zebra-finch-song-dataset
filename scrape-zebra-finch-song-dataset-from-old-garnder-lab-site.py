#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pathlib
import urllib.parse

from bs4 import BeautifulSoup
import pandas as pd
import requests


# In[2]:


URL = 'https://people.bu.edu/timothyg/song_website/index.html'


# In[3]:


page = requests.get(URL)


# In[4]:


soup = BeautifulSoup(page.content, "html.parser")


# In[5]:


def wav_path_from_number(wav_number: int):
    return f"https://people.bu.edu/timothyg/song_website/WAV/{wav_number}.wav"


# In[6]:


labs = soup.find_all("h2")[1:]


# ## Get all the wav paths

# In[8]:


results = {}
for lab in labs:
    wav_paths = []
    for sibling in lab.find_next_siblings():
        if sibling.name == "h2" or sibling.name == "h3":
            break
        wav_number = int(sibling.text.split('_')[-1])
        wav_path = wav_path_from_number(wav_number)
        wav_paths.append(wav_path)
    results[lab.text] = wav_paths


# ## Save the wav files, make a csv

# In[15]:


records = []

for lab, wav_paths in results.items():
    lab_dir = pathlib.Path(f'./data/{lab}')
    lab_dir.mkdir(exist_ok=True)
    for wav_path in wav_paths:
        url_parsed = urllib.parse.urlparse(wav_path)
        wav_name = pathlib.Path(urllib.parse.unquote(url_parsed.path)).name
        local_path = lab_dir / wav_name
        with open(local_path, 'wb') as fp:
            response = requests.get(wav_path)
            if response.status_code == 200:
                fp.write(response.content)
                print(f'downloaded: {wav_path}')
            else:
                print(resp.reason)
                exit(1)
        records.append(
            {
                "lab": lab,
                "wav_path": wav_path,
                "wav_name": wav_name,
                "local_path": local_path
            }
        )


# In[16]:


df = pd.DataFrame.from_records(records)


# In[19]:


df.to_csv('./data/zebra-finch-5labs-227birds-song-dataset.csv')

