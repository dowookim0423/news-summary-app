import os
import requests
from bs4 import BeautifulSoup

# 네이버 뉴스 검색 (정치 분야, 최신 5개 뉴스)
def naver_news_search(query="정치"):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("환경변수 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 설정이 필요합니다.")
        return []

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": 5,
        "sort": "date"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("뉴스 검색 실패:", response.status_code)
        return []

    data = response.json()
    return data.get("items", [])

# 네이버 뉴스 기사 본문 크롤링
def crawl_article_content(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
    except Exception as e:
        print(f"기사 본문 불러오기 실패: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 네이버 뉴스 본문 선택자 (네이버 뉴스 레이아웃에 따라 바뀔 수 있음)
    article_body = soup.select_one("#dic_area")
    if not article_body:
        # 레이아웃 변경 대비 다른 시도 (네이버 뉴스 경우)
        article_body = soup.select_one(".news_end")

    if not article_body:
        print("본문 영역을 찾을 수 없습니다.")
        return None

    content = article_body.get_text(strip=True, separator="\n")
    return content

# 간단 요약 함수 (예시: 첫 3문장만 리턴)
def summarize_text(text, sentence_count=3):
    sentences = text.split('.')
    summary = '.'.join(sentences[:sentence_count]).strip()
    if not summary.endswith('.'):
        summary += '.'
    return summary

# 메인 실행 함수
def main():
    print("=== 네이버 뉴스 '정치' 분야 최신 뉴스 5개 ===")
    news_items = naver_news_search("정치")

    if not news_items:
        print("뉴스 검색 결과가 없습니다.")
        return

    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item['title'].replace('&quot;', '\"').replace('&amp;', '&')}")
        print(f"   링크: {item['link']}")

    article_url = input("\n요약할 기사 URL을 입력하세요: ").strip()
    print("\n기사 본문 크롤링 중...")
    content = crawl_article_content(article_url)

    if content:
        print("\n✅ 기사 본문 요약:")
        summary = summarize_text(content)
        print(summary)
    else:
        print("본문을 크롤링하지 못했습니다.")

if __name__ == "__main__":
    main()
