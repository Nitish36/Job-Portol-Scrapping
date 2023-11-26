import requests
from bs4 import BeautifulSoup


job_links = 'https://www.timesjobs.com/job-detail/python-engineer-east-india-securities-ltd-kolkata-2-to-5-yrs-jobid-KEkE19WqPbFzpSvf__PLUS__uAgZw==&source=srp'
html_text = requests.get(job_links).text
soup = BeautifulSoup(html_text, 'html.parser')
Web = soup.find('ul',class_ = 'hirng-comp-oth clearfix')
website = Web.find('a')['href']
print(website)
