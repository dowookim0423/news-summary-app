import requests
from bs4 import BeautifulSoup

def crawl_rss_news():
    rss_url = "https://www.yna.co.kr/rss/politics.xml"
    response = requests.get(rss_url)
    if response.status_code != 200:
        print("RSS 피드 불러오는데 실패했습니다.")
        return

    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")[:5]

    print("정치 뉴스 최신 제목 5개:")
    for i, item in enumerate(items, 1):
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        print(f"{i}. {title}")
        print(f"   링크: {link}")

if __name__ == "__main__":
    crawl_rss_news()
