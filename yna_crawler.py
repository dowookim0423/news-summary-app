import requests
from bs4 import BeautifulSoup

def get_article_links(keyword, page=1):
    url = f"https://www.yna.co.kr/search/index?query={keyword}&page={page}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    links = []
    for tag in soup.select('.cts_atcl > a'):
        href = tag.get('href')
        if href and href.startswith('https://www.yna.co.kr/view/'):
            links.append(href)
    return links

def get_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    title = soup.select_one('h1.tit')
    body = soup.select_one('.article-txt')
    
    return {
        'title': title.get_text(strip=True) if title else '',
        'body': body.get_text(strip=True) if body else ''
    }

# 🔍 테스트 실행
if __name__ == "__main__":
    keyword = "인공지능"
    links = get_article_links(keyword)
    
    for link in links[:3]:  # 3개만 시범적으로 출력
        article = get_article_content(link)
        print("제목:", article['title'])
        print("본문:", article['body'][:200], '...\n')  # 본문 일부 출력
