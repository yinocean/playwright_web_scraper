from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class Wanted_scraper():
    def playwright_scrape(skill):
        print(f"{skill} 시작")
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto("https://www.wanted.co.kr/jobsfeed")
        time.sleep(7)

        page.click("button.Aside_searchButton__Xhqq3 ")
        time.sleep(5)

        page.get_by_placeholder("검색어를 입력해 주세요.").fill(f"{skill}")

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
        print(f"{skill} 완료")
        return jobs_db
        
    def file_save(skill, jobs_db):
        print(f"{skill} 이름")
        file = open(file=f"{skill}.csv", mode="w", encoding="utf-8")
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


if __name__ == "__main__":
    keywords = [
    "python",
    "nextjs",
    "kotlin",
    "flutter",
]
    for keyword in keywords:
        scrape = Wanted_scraper.playwright_scrape(keyword)
        Wanted_scraper.file_save(keyword, scrape)