from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


p = sync_playwright().start()  # initialize playwright
browser = p.chromium.launch(headless=False)  # initialize browser
page = browser.new_page()  # create a new tab


page.goto('https://www.wanted.co.kr/search?query=%ED%94%84%EB%A1%A0%ED%8A%B8&tab=position')

time.sleep(3)

for i in range(4):
    page.keyboard.down('End')
    time.sleep(3)

html = page.content()

p.stop()

soup = BeautifulSoup(html, 'html.parser')

jobs = soup.find_all('div', class_='JobCard_container__REty8')
jobs_db = []
base_url = 'https://www.wanted.co.kr/'

for job in jobs:
    link = f"{base_url}{job.find('a')['href']}"
    title = job.find('strong', class_='JobCard_title__HBpZf').text
    company_name = job.find('span', class_='JobCard_companyName__N1YrF').text
    reward = job.find('span', class_='JobCard_reward__cNlG5').text
    data = {
        'title': title,
        'company_name': company_name,
        'link': link,
        'reward': reward,
    }
    jobs_db.append(data)


file = open('jobs.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Link', 'Reward'])

for job in jobs_db:
    writer.writerow(job.values())

file.close()