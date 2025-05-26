import requests
from bs4 import BeautifulSoup

def get_naver_article_summary(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("네이버 뉴스 페이지 요청 실패")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 네이버 뉴스 본문 영역
    content_div = soup.find("article", id="dic_area")
    if not content_div:
        print("본문을 찾지 못했습니다.")
        return None

    # 전체 본문 텍스트
    full_text = content_div.get_text(separator="\n", strip=True)
    paragraphs = full_text.split("\n")

    # 앞 2~3 문단만 요약으로 추출
    summary = "\n".join(paragraphs[:3])  # 원한다면 [:2]로 줄여도 됨
    return summary

if __name__ == "__main__":
    url = input("네이버 뉴스 기사 URL을 입력하세요:\n> ")
    summary = get_naver_article_summary(url)
    if summary:
        print("\n✅ 기사 요약 내용:")
        print(summary)
