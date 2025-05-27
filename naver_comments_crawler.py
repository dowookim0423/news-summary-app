import requests
import json
import re

def extract_comments(oid, aid, page=1):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = (
        f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json"
        f"?ticket=news&templateId=default_news&pool=cbox5&lang=ko&country=KR"
        f"&objectId=news{oid},{aid}&pageSize=20&page={page}&sort=newest"
    )

    response = requests.get(url, headers=headers)
    
    # JSONP 형식 → JSON으로 변환
    try:
        json_str = re.search(r"_callback\((.*)\)", response.text).group(1)
        data = json.loads(json_str)
        comments = data['result']['commentList']
        return [comment['contents'] for comment in comments]
    except Exception as e:
        print("❌ 댓글을 가져오는데 실패했습니다:", e)
        return []

if __name__ == "__main__":
    url = input("네이버 뉴스 기사 URL을 입력하세요:\n> ").strip()

    # 예: https://n.news.naver.com/mnews/article/001/0014603349
    match = re.search(r'article/(\d+)/(\d+)', url)
    if not match:
        print("❌ 올바른 네이버 뉴스 URL을 입력하세요.")
    else:
        oid, aid = match.group(1), match.group(2)
        comments = extract_comments(oid, aid)
        
        print("\n✅ 수집된 댓글 목록:")
        for i, comment in enumerate(comments, 1):
            print(f"{i}. {comment}")
