import requests
from bs4 import BeautifulSoup

def crawl_rss_news():
    rss_url = "https://rss.etoday.co.kr/newssection.xml?section=section03"  # 이투데이 정치 뉴스 RSS
    response = requests.get(rss_url)
    if response.status_code != 200:
        print("RSS를 불러오는데 실패했습니다.")
        return

    soup = BeautifulSoup(response.content, "xml")  # RSS는 XML 형식
    items = soup.find_all("item")[:5]  # 최신 뉴스 5개

    print("정치 뉴스 최신 제목 5개 (이투데이 RSS):")
    for i, item in enumerate(items, 1):
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        print(f"{i}. {title}")
        print(f"   링크: {link}")

if __name__ == "__main__":
    crawl_rss_news()
