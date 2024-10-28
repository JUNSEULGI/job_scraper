from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class Scraper():

    def __init__(self):
        self.base_url = 'https://www.wanted.co.kr/'


    def extract_job_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_='JobCard_container__REty8')
        jobs_db = []

        for job in jobs:
            link = f"{self.base_url}{job.find('a')['href']}"
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

        return jobs_db


    def convert_to_excel(self, name, data):
        file = open(f'{name}.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Link', 'Reward'])

        for job in data:
            writer.writerow(job.values())

        file.close()


    def scrape_page(self, keyword):
        p = sync_playwright().start()  # initialize playwright
        browser = p.chromium.launch(headless=False)  # initialize browser
        page = browser.new_page()  # create a new tab
        page.goto(f'{self.base_url}search?query={keyword}&tab=position')
        time.sleep(3)

        for _ in range(4):
            page.keyboard.down('End')
            time.sleep(3)

        html = page.content()
        p.stop()

        jobs_db = self.extract_job_data(html)
        self.convert_to_excel(keyword, jobs_db)

    
    def search_jobs_by_keywords(self, keywords):
        for keyword in keywords:
            self.scrape_page(keyword)


keywords = ['flutter', 'kotlin', 'nextjs']
job_scraper = Scraper()
job_scraper.search_jobs_by_keywords(keywords)