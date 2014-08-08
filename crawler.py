import urllib
import os
import fetchInfo
import requests
from bs4 import BeautifulSoup
'''
base_url = "http://www.tripadvisor.com"

dir = "D:\\Reviews\\"

hotel_list_url = base_url + "/Hotels-g60763-New_York_City_New_York-Hotels.html"


urls = [hotel_list_url]    #stack of urls to use
visitied = [hotel_list_url]    #historic records of urls

while len(urls) > 0:
    
    try:
        
        html_text = urllib.urlopen(urls[0]).read()
        
    except:
        
        print urls[0]
        continue
    
    soup = BeautifulSoup(html_text)
    urls.pop(0)
    
    for hotel in soup.findAll('a',{'class' : 'property_title'}):
        hotel_name = hotel.string[1:].replace(replace_sign[0][0],replace_sign[0][1])        #standardlize file name
        print hotel_name
        file_path = os.path.join(dir,hotel_name + ".txt")
        hotel_review_url = base_url + hotel['href']         #hotel review url
        review = fetchInfo.FetchInfo.parse(hotel_name,hotel_review_url)
        fileHandle = open(file_path, 'w')
        title = review.txt_title
        
        fileHandle.write(title)
        fileHandle.close()
'''
''''
url = 'http://www.tripadvisor.com/Hotel_Review-g60763-d113317-Reviews-Casablanca_Hotel_Times_Square-New_York_City_New_York.html'
post_url = 'http://www.tripadvisor.com/SortReviews'
r = requests.get(url)
html = BeautifulSoup(r.content)
dict = {}
returnTo = str(html.find('input',{'name': 'returnTo'})['value'])
filterRating = "0"
filterSegment = "3"
dict['&returnTo='] = returnTo
dict['&filterRating='] = filterRating
dict['filterSegment='] = filterSegment
params = "?"
for key,value in dict.items():
    params = params + key + value
print params
post_url = post_url + params
print post_url
r = requests.get(post_url)
sub_html = BeautifulSoup(r.content)
for data in sub_html.findAll('div',{'class' : 'wrap row'}):
    count = data.find('span',{'class': 'compositeCount'}).string
    print count
'''