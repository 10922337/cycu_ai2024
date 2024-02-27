print('Hello, World!')

#https://news.pts.org.tw/xml/newsfeed.xml
import requests
import feedparser

url = "https://news.pts.org.tw/xml/newsfeed.xml"

response = requests.get(url)

feed = feedparser.parse(response.content)

for entry in feed.entries:
    print(entry.title)
    print(entry.summary)

    if '日' in entry.summary:
        with open('C:/Users/User/Desktop/news.csv', 'a', encoding='utf-8-sig') as file:
            file.write(entry.title + '\n')
            file.write(entry.summary + '\n')
            file.write('=================================')

    print("==================================")