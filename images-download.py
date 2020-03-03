#!/usr/bin/env python
# coding: utf-8

# In[8]:


get_ipython().system('pip install selenium')


# In[9]:


"""
Testing working 
"""
"""
from selenium import webdriver
chromedriver = 'C:\chromedriver80\chromedriver.exe'

driver = webdriver.Chrome(chromedriver)

driver.get("https://www.nytimes.com")
headlines = driver.find_elements_by_class_name("story-heading")
for headline in headlines:
    print(headline.text.strip())
"""


# In[10]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import json
import os
import argparse
import sys

import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import datetime
import time


# In[11]:


urllib3.disable_warnings(InsecureRequestWarning)
chromedriver = 'C:\chromedriver80\chromedriver.exe'


# In[12]:


def download_google_staticimages(searchurl,dirs):

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument('--headless')

    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'chromedriver not found in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting a lot of images. This may take a while')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    #for i in range(30):
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    print(f'Reached end of page.')
    time.sleep(0.5)
    print(f'Retry')
    time.sleep(0.5)

    # Below is in "show more result" sentence. Change this word to your lanaguage if you require.
    browser.find_element_by_xpath('//input[@value="Show more results"]').click()

    # Scroll down 2
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    #elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    #page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source 

    soup = BeautifulSoup(page_source, 'html.parser')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

    count = 0
    if urls:
        for url in urls:
            try:
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                    f.write(rawdata)
                    #print('downloading img_' + str(count) + '.jpg\n')
                    print(".")
                    count += 1
                    """if ((count>= maxcount) and (maxcount != 0)):
                        print("Set limit reached")
                        return count
                    """
            except Exception as e:
                print('Failed to write rawdata.')
                print(e)

    browser.close()
    return count


# In[13]:


# Main block
def main():
    """
    input activities
    """
    print("\nEnter search keyword(s):")
    searchword = str(input())
    #print("\nEnter number of images to download. Enter 0 to download as many as possible:")
    #maxcount = int(input())
    maxcount = 1
    print("\nEnter name of directory where the downloaded images will be saved:")
    dirs = str(input())
    
    
    searchurl = 'https://www.google.com/search?q=' + searchword +  '&source=lnms&tbm=isch'
    
    if not os.path.exists(dirs):
        os.mkdir(dirs)
    
    t0 = time.time()
    count = download_google_staticimages(searchurl,dirs)
    t1 = time.time()

    total_time = t1 - t0
    print(f'\n')
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')


# In[14]:


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




