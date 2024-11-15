from requests_html import HTMLSession

def fetch_google_news(company, country, time_range="when:1y"):
    session = HTMLSession()
    
    query = f"{company}+{country}+{time_range}"
    url = f'https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en'
    
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=3)  
    
    articles = r.html.find('article')
    news_items = []

    for item in articles:
        news_item = item.find('a', first=True)
        if news_item:
            title = news_item.text
            link = list(news_item.absolute_links)[0] if news_item.absolute_links else None
            news_items.append({'title': title, 'link': link})
            print(f"Title: {title}, Link: {link}")

    return news_items

company = "Oracle"
country = "Nigeria"
articles = fetch_google_news(company, country, "when:1y")
