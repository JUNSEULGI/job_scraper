from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

p = sync_playwright().start()  # initialize playwright
browser = p.chromium.launch(headless=False)  # initialize browser
page = browser.new_page()  # create a new tab

url = 'https://www.wanted.co.kr/'

page.goto('https://www.wanted.co.kr/')

time.sleep(3)

page.click('button.Aside_searchButton__rajGo')

time.sleep(3)

page.get_by_placeholder('검색어를 입력해 주세요.').fill('프론트')

time.sleep(3)

page.keyboard.down('Enter')

time.sleep(5)

page.click('a#search_tab_position')

time.sleep(3)

for i in range(4):
    page.keyboard.down('End')
    time.sleep(3)

html = page.content()

p.stop()

soup = BeautifulSoup(html, 'html.parser')

jobs = soup.find_all('div', class_='JobCard_container__REty8')
jobs_db = []

for job in jobs:
    link = f"{url}{job.find('a')['href']}"
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

print(len(jobs_db))
print(jobs_db)