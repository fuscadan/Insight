'''
    This is a script to clean and preprocess NBA game recaps scraped from espn.com.
'''

#dev code to get an example soup file to parse
import urllib3 
import certifi
from bs4 import BeautifulSoup 

#test_soup_file = 'Git/scripts/test_soup.txt' 

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())


url = 'https://www.espn.com/nba/recap?gameId=400899380' 
r = http.request('GET', url) 
soup = BeautifulSoup(r.data, 'html.parser') 

article_tag = soup.select('.article-body')[0]

paragraphs = article_tag.find_all('p')

article = []

for i in range(len(paragraphs)):
    article.append(paragraphs[i].get_text())

