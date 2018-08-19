import urllib.request
from bs4 import BeautifulSoup
import re


def getSoup(url):
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request, timeout=20)
	content = response.read()
	soup = BeautifulSoup(content, 'html.parser')
	return soup


def getWordListUrls(soup):
	wordLists = []
	div = soup.find(id='wordbook-wordlist-container')
	wordListsDiv = div.find_all('tr')

	for wordListDiv in wordListsDiv:
		url = 'https://www.shanbay.com/'
		title = ''
		if (wordListDiv.a != None):
			aTag = wordListDiv.a
			
			# Get wordList full URL
			url += aTag['href']
			
			# Get wordList title(name)
			title = aTag.string
			wordCount = wordListDiv.find("td", class_="wordbook-wordlist-count")
			
			# Get wordList count 
			count = int(re.findall(r'\d+', wordCount.text.strip())[0])
			
			# append list data to urls list and return for next step
			wordLists.append([url, title, count])
	print(wordLists)

		
		
	

def main():
	url = 'https://www.shanbay.com/wordbook/102106/'
	soup = getSoup(url)
	getWordListUrls(soup)
	
main()
	