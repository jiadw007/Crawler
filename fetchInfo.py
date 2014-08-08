import requests
from bs4 import BeautifulSoup
from review import Review


class FetchInfo():
    
    
    post_url = 'http://www.tripadvisor.com/SortReviews'
    segment_list = ["filterSegment=3","filterSegment=2","filterSegment=5","filterSegment=1"]
    def __init__(self,url,hotel_name):
        self.url = url
        self.hotel_name = hotel_name
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)
        self.returnTo = str(self.soup.find('input',{'name': 'returnTo'})['value'])
    
    def fetch_html(self):
        '''build soup'''
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)
        
    
    def fetch_thumb_up(self):
        '''fetch thumb up'''
        thumb_up = self.soup.find('span',{'class':'percent'})
        while thumb_up is None:
            self.fetch_html()
            thumb_up = self.fetch_thumb_up()
        return thumb_up
    
    def fetch_rank(self):
        '''fetch rank'''
        rank = self.soup.find('b', {'class': 'rank_text'})
        while rank is None:
            self.fetch_html()
            rank = FetchInfo.fetch_rank()
            
        return rank
    
    def fetch_total_reviews(self):
        '''fetch total_reviews'''
        total_reviews = self.soup.find('span', {'property':'v:count'}).string
        while total_reviews is None:
            self.fetch_html()
            total_reviews = self.fetch_total_reviews()
        #result = ''.join(total_reviews.split(','))
        return total_reviews
    
    
    def fetch_sub_reviews(self, rev, i):
        
        values = "segment segment" + str(i)
        #print values
        tag = self.soup.find('div',{'class' : values})
        count = tag.find('div', {'class' : 'value'}).string
        #sub total review
        rev.table[i].append(str(count))
        params = "?" + FetchInfo.segment_list[i-1] + "&returnTo=" + self.returnTo + "&filterRating=0"
        post_url = FetchInfo.post_url + params
        #print post_url
        request = requests.get(post_url)
        html = BeautifulSoup(request.content)
        for data in html.findAll('div',{'class' : 'wrap row'}):
            nums = data.find('span',{'class': 'compositeCount'}).string
            rev.table[i].append(str(nums))
            
    
    
    def fetch_rating(self,rev,index):
        '''fetch rating'''
        summary_box = self.soup.find('div', {'id' : 'SUMMARYBOX'})
        for data in summary_box.findAll('img', {'class' : 'sprite-rating_s_fill'}):
            summary = data['alt'].split(' ')
            rev.table[index].append(summary[0])
        
    
    def fetch_review_properties(self, rev, total, index):
        '''build two demension table'''
        
        
        if index == 0:
            rev.table[index].append(total)
            for data in self.soup.findAll('div',{'class' : 'wrap row'}):
                count = data.find('span',{'class': 'compositeCount'}).string
                rev.table[index].append(count)
        else:
            ##fetch information after click on families,Couples,Solo, Business
            self.fetch_sub_reviews(rev,index)
        self.fetch_rating(rev,index)


       
url_path = "http://www.tripadvisor.com/Hotel_Review-g60763-d113317-Reviews-Casablanca_Hotel_Times_Square-New_York_City_New_York.html"
hotel_name = "Casablanca Hotel Times Square"

##Initialize
fetch = FetchInfo(url_path,hotel_name)
##fetch thumb_up rank and total_reviews
thumb_up = fetch.fetch_thumb_up() #thumb up
rank =  fetch.fetch_rank()  #rank
total_reviews = fetch.fetch_total_reviews()   #total_reviews

##construct Review object       
txt_title = """%s, %s, %s, %s """ %(hotel_name, thumb_up.string, rank.string, str(total_reviews) + " Reviews") # txt_title
rev  = Review(txt_title) #Review Object

##fill all review properties in the reviewers
i = 0
while i <= 4:
    
    fetch.fetch_review_properties(rev,total = total_reviews, index = i)
    i = i + 1       
rev.write_into_file(hotel_name)























