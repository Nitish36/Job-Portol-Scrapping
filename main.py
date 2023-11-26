import requests
from bs4 import BeautifulSoup
import pandas as pd
# List of job search result URLs
job_data_list = []
flag = 0
keywords = ['python', 'java', 'html', 'CSS', 'JavaScript', 'sql', 'devops', 'xml','excel']
for flag in range(0,len(keywords)):
    for link in range(1,11,1):
        job_links = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keywords[flag]}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keywords[flag]}&searchBy=0&rdoOperator=OR&pDate=I&sequence={link}&startPage=1'
        html_text = requests.get(job_links).text
        soup = BeautifulSoup(html_text, 'html.parser')
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        for job in jobs:
            job_name = job.find('h2').text.strip()
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            url_extract = job.find('a')['href']
            text = requests.get(url_extract).text
            soup2 = BeautifulSoup(text,'html.parser')
            JD = soup2.find('div',class_='jd-desc job-description-main').text.replace("Job Description","").strip()
            list_items = soup2.find('ul', {'class': 'clearfix', 'id': 'applyFlowHideDetails_1'}).find_all('li')
            # Loop through each list item and extract label and value
            label_value_pairs = {}
            for item in list_items:
                label_element = item.find('label')
                if label_element is not None:
                    label = label_element.text.strip()
                    value_element = item.find('span', {'class': 'basic-info-dtl'})
                    if value_element is not None:
                        value = value_element.text.strip()
                        label_value_pairs[label] = value
            skills = job.find('span', class_='srp-skills').text.replace(' ', '').strip()
            date_posted = job.find('span', class_='sim-posted').text.strip()
            YOE = job.find('li').text.replace('card_travel','')
            location = job.find('span').text.strip()
            Web = soup2.find('ul', class_='hirng-comp-oth clearfix')
            website = None  # Default to None if website isn't found
            if Web is not None:
                anchor = Web.find('a')
                if anchor is not None and 'href' in anchor.attrs:
                    website = anchor['href']
            job_data = {
                'Job Name': job_name,
                'Company Name': company_name,
                'JD': JD,
                'Skills': skills,
                'Date Posted': date_posted,
                'YOE': str(YOE).zfill(2),
                'Location': location,
                'Website':website,
                **label_value_pairs
            }
            job_data_list.append(job_data)
        #if link >= 10:
        #    link = 1



dataset = pd.DataFrame(job_data_list)
#dataset.drop(['Hiring Location:','Role:'],)
dataset.to_csv("Scrapped_data.csv",index = 0)
print('Dataset Generated Successfully.....')

#
########### Introduction ################
'''
with open('home.html','r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content,'lxml')
    
    course_html_tags = soup.find_all('h5')
    for course in course_html_tags:
        print(course.text)
    course_cards = soup.find_all('div',class_ = 'card')
    for course in course_cards:
        #print(course.h5.text,":",course.a.text)
        price = course.a.text.split()[-1]
        print(course.h5.text, ":", price)
    
'''