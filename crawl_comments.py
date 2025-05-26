import requests
import re
import json

def extract_article_id(url):
    match = re.search(r'/view/AKR(\d+)', url)
    if match:
        return match.group(1)
    return None

def crawl_comments(article_id):
    api_url = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json"
    params = {
        "ticket": "news",
        "templateId": "default_politics",
        "pool": "cbox5",
        "lang": "ko",
        "country": "KR",
        "objectId": f"newsAKR{article_id}",  # AKR 포함해야 작동함
        "pageSize": 10,
        "page": 1,
        "sort": "new"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        print("댓글 API 요청 실패")
        return []

    # JSONP 응답 처리: 괄호 안의 JSON만 추출
    match = re.search(r'\((\{.*\})\)', response.text)
    if not match:
        print("JSON 추출 실패 (JSONP 형식 아님)")
        return []

    try:
        json_data = json.loads(match.group(1))
        comment_items = json_data.get('result', {}).get('commentList', [])
        return [c['contents'] for c in comment_items]
    except Exception as e:
        print("JSON 파싱 실패:", e)
        return []

if __name__ == "__main__":
    # 예시 연합뉴스 기사 URL
    news_url = "https://www.yna.co.kr/view/AKR20250526071851001"
    article_id = extract_article_id(news_url)

    if article_id:
        comments = crawl_comments(article_id)
        if comments:
            print(f"댓글 {len(comments)}개 수집됨:")
            for i, comment in enumerate(comments, 1):
                print(f"{i}. {comment}")
        else:
            print("댓글 없음 또는 추출 실패")
    else:
        print("article_id 추출 실패")
