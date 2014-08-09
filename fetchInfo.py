import requests
from bs4 import BeautifulSoup
from review import Review


class FetchInfo():
    
    
    post_url = 'http://www.tripadvisor.com/SortReviews'
    segment_list = ["filterSegment=3","filterSegment=2","filterSegment=5","filterSegment=1"]
    def __init__(self,url):
        self.url = url
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
        if thumb_up is None:
            return "of travelers recommend"
        else:
            return thumb_up.string
    
    def fetch_rank(self):
        '''fetch rank'''
        rank = self.soup.find('b', {'class': 'rank_text'})
        while rank is None:
            self.fetch_html()
            print "error"
            rank = self.fetch_rank()
            
        return rank.string
    
    def fetch_address(self):
        '''fetch address'''
        ##print self.soup
        address =""
        tags = self.soup.find('span',{'rel':'v:address'})
        for tag in tags.findAll('span'):
            if tag.string is not None:
                loc = tag.string.replace(',',' ')
                address = address + " " + loc
        return address
    
        
    
    def fetch_total_reviews(self):
        '''fetch total_reviews'''
        total_reviews = self.soup.find('span', {'property':'v:count'}).string
        while total_reviews is None:
            self.fetch_html()
            total_reviews = self.fetch_total_reviews()
        #result = ''.join(total_reviews.split(','))
        return total_reviews
    
    
    def fetch_sub_reviews(self, rev, i):
        '''fetch sub reviews for different group'''
        values = "segment segment" + str(i)
        #print values
        tag = self.soup.find('div',{'class' : values})
        count = tag.find('div', {'class' : 'value'}).string.replace(',','')
        ##sub total review
        rev.table[i].append(count)
        params = "?" + FetchInfo.segment_list[i-1] + "&returnTo=" + self.returnTo + "&filterRating=0"
        post_url = FetchInfo.post_url + params
        #print post_url
        request = requests.get(post_url)
        html = BeautifulSoup(request.content)
        for data in html.findAll('div',{'class' : 'wrap row'}):
            nums = data.find('span',{'class': 'compositeCount'}).string.replace(',','')
            rev.table[i].append(nums)
            
    
    
    def fetch_rating(self,rev,index):
        '''fetch rating'''
        summary_box = self.soup.find('div', {'id' : 'SUMMARYBOX'})
        for data in summary_box.findAll('img', {'class' : 'sprite-rating_s_fill'}):
            summary = data['alt'].split(' ')
            rev.table[index].append(summary[0])
        
    
    def fetch_review_properties(self, rev, total, index):
        '''build two demensions table'''
        
        if index == 0:
            
            rev.table[index].append(total.replace(',',''))
            for data in self.soup.findAll('div',{'class' : 'wrap row'}):
                count = data.find('span',{'class': 'compositeCount'}).string
                rev.table[index].append(count.replace(',',''))
        else:
            ##fetch information after click on families,Couples,Solo, Business
            self.fetch_sub_reviews(rev,index)
        self.fetch_rating(rev,index)


       
























