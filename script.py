import urllib.request
from bs4 import BeautifulSoup
import re
import math


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
#	print(wordLists)
	return wordLists
	
	
def getWords(wordLists):
	allWords = []
	for wordList in wordLists:
		allWords.append('#' + wordList[1])
		pageNum = math.ceil(wordList[2] / 20)
		for i in range(1, pageNum+1):
			soup = getSoup(wordList[0] + '?page=' + str(i))
			wordRows = soup.table.find_all('tr')
			for wordRow in wordRows:
				allWords.append(wordRow.strong.string)
	return allWords
		


def writeTxt(words):
	with open('list.txt', 'w') as f:
		for word in words:
			f.write(word + '\n')	
		
	

def main():
	url = 'https://www.shanbay.com/wordbook/1576/'
	soup = getSoup(url)
	wordLists = getWordListUrls(soup)
	allWords = getWords(wordLists)
	writeTxt(allWords)
	
main()
	