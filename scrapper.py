#beautifulsoup imports
import requests
from bs4 import BeautifulSoup

scraped_jobs=[]

#selenium imports
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ScreenshotException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd

def extract(page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
    url = f"https://de.indeed.com/jobs?q=bioinformatics&l=munich&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def transform(soup):
    divs = soup.find_all('div', {'class': "job_seen_beacon"})
    for i in divs:
        title = i.find('span').text.strip()
        
        title_desc = title
        if 'bioinformatics' in title_desc:
            title_desc = 'Bioinformatics'
        if 'computational' in title_desc:
            title_desc = 'Computational Biology'
        else:
            title_desc = title_desc

        company = i.find('span', {'class': 'companyName'}).text.strip()
        if 'Universität' in company:
            company = 'University'
        else:
            company = 'Company'
        try:
            rating = i.find('span', {"class": "ratingNumber"}).text.strip()
        except:
            rating = ''
        
        location = i.find('div', {'class': "companyLocation"}).text.strip()
        
        desc_Degree = i.find('div', {'class': "job-snippet"}).text.strip()
        if 'MSc' in desc_Degree:
            desc_Degree = 'MSc'
            break
        if 'PhD' in desc_Degree:
            desc_Degree = 'PhD'
        
        desc_Title = i.find('div', {'class': "job-snippet"}).text.strip()
                

        Summary = {
            'Title' : title,
            'Job Title': title_desc,
            'Company': company,
            'Rating': rating,
            'Location': location,
            'Degree': desc_Degree
        }
        scraped_jobs.append(Summary)
        print(Summary)
    return


#for i in range(0,30,10):
    #print(f'Getting page, {i}')
    #c = extract(0)
    #transform(c)

c = extract(0)
transform(c)
print(scraped_jobs)
#print(len(scraped_jobs))

#final_data = pd.DataFrame(scraped_jobs)
#final_data.to_csv('final_data.csv')