from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()
page.goto("https://www.wanted.co.kr/jobsfeed")
time.sleep(7)

page.click("button.Aside_searchButton__Xhqq3 ")
time.sleep(5)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

time.sleep(5)
page.keyboard.down("Enter")
time.sleep(5)

page.click("a#search_tab_position")



for x in range(7):
    time.sleep(5)
    page.keyboard.down('End')

content = page.content()
p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all('div', class_ = "JobCard_container__FqChn")

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
    title = job.find("strong", class_ = "JobCard_title__ddkwM").text
    company_name = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
    reward = job.find("span", class_ = "JobCard_reward__sdyHn").text
    job = {
        "title" : title,
        "company_name" : company_name,
        "reward" : reward,
        "link" : link
    }
    jobs_db.append(job)

# #print(jobs_db)
# #print(len(jobs_db))

file = open("jobs.csv", mode="w", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(
    [
    "Title",
    "Company_name",
    "Reward",
    "Link",
    ]
)
for job in jobs_db:
    writer.writerow(job.values())
    
file.close()