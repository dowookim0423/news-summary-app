import os
import sys
import requests

def naver_news_search(query, display=5, start=1):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("환경변수 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET을 설정해주세요.")
        sys.exit(1)

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": "date"  # 최신순 정렬
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    return data.get("items", [])

if __name__ == "__main__":
    keyword = "정치"  # 원하는 검색어
    news_items = naver_news_search(keyword)

    print(f"네이버 뉴스 '{keyword}' 검색 결과:")
    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item['title'].replace('<b>', '').replace('</b>', '')}")
        print(f"   {item['originallink']}")
