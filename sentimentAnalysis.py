import csv
import json
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def getNewsData(company_name):
    search_query = f"news {company_name} in Nigeria"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(
        f"https://www.google.com/search?q={search_query.replace(' ', '+')}&gl=ng&tbm=nws&num=100", headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []

    for el in soup.select("div.SoaBEf"):
        title_element = el.select_one("div.MBeuO")
        snippet_element = el.select_one(".GI74Re")
        date_element = el.select_one(".LfVVr")
        source_element = el.select_one(".NUnG9d span")

        if title_element and snippet_element and date_element and source_element:
            link = el.find("a")["href"]
            news_results.append({
                "link": link,
                "title": title_element.get_text(),
                "snippet": snippet_element.get_text(),
                "date": date_element.get_text(),
                "source": source_element.get_text()
            })

   
    with open("news_links.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link", "date", "source", "snippet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in news_results:
            writer.writerow(article)

    print("News links saved to news_links.csv")
    average_sentiment = analyze_sentiment(news_results)
    print(f"\nFinal Average Sentiment Score: {average_sentiment:.2f}")

def analyze_sentiment(news_results):
    total_sentiment = 0
    article_count = 0

    for article in news_results:
        try:
            response = requests.get(article["link"])
            content = response.text
            
            soup = BeautifulSoup(content, "html.parser")
            paragraphs = soup.find_all("p")
            full_text = " ".join([para.get_text() for para in paragraphs])

            analysis = TextBlob(full_text)
            sentiment = analysis.sentiment.polarity 

            total_sentiment += sentiment
            article_count += 1

            print(f"URL: {article['link']}, Sentiment: {sentiment:.2f}")
        except Exception as e:
            print(f"Failed to process {article['link']}: {e}")

   
    if article_count > 0:
        average_sentiment = total_sentiment / article_count
    else:
        average_sentiment = 0  

    return average_sentiment


company_name = input("Enter the name of the company: ")
getNewsData(company_name)
