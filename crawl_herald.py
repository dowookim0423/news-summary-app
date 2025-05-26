import requests
from bs4 import BeautifulSoup

def crawl_herald():
    url = "https://www.heraldcorp.com/politics"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    print("Response status:", response.status_code)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.news_list > ul > li")

    print("Number of articles found:", len(articles))

    news_list = []

    for article in articles[:10]:
        link_tag = article.select_one("a")
        if link_tag:
            title = link_tag.get_text(strip=True)
            link = link_tag["href"]
            if link.startswith("/"):
                link = "https://www.heraldcorp.com" + link
            news_list.append({
                "title": title,
                "link": link
            })

    return news_list

if __name__ == "__main__":
    news = crawl_herald()
    for idx, item in enumerate(news, start=1):
        print(f"{idx}. {item['title']}\n   {item['link']}\n")

