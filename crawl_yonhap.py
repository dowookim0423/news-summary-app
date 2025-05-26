import requests
from bs4 import BeautifulSoup

def crawl_yonhap():
    url = "https://www.yna.co.kr/politics"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://www.yna.co.kr/",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, headers=headers)
    print("Response status:", response.status_code)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.list-type038 > ul > li")
    print("Number of articles found:", len(articles))

    news_list = []

    for article in articles[:10]:
        title_tag = article.select_one("strong.tit-news")
        link_tag = article.select_one("a")

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = link_tag["href"]
            news_list.append({
                "title": title,
                "link": link
            })

    return news_list

if __name__ == "__main__":
    news = crawl_yonhap()
    for idx, item in enumerate(news, start=1):
        print(f"{idx}. {item['title']}\n   {item['link']}\n")
