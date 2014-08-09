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
        
    
    def fetch_thumb_up(self):##exception finish
        
        '''fetch thumb up'''
        thumb_up = self.soup.find('span',{'class':'percent'})
        tries = 2
        while thumb_up is None and tries > 0:
            
            self.fetch_html()
            print "thumb_up failed, one more time"
            thumb_up = self.soup.find('span',{'class':'percent'})
            tries = tries - 1
            
        if thumb_up is None:
            print "0% of travelers recommend"
            return "0%"
        else:
            return thumb_up.string
    
    def fetch_rank(self): ##exception finish
        
        '''fetch rank'''
        rank = self.soup.find('b', {'class': 'rank_text'})
        
        tries = 2
        while rank is None and tries > 0:
            
            print "rank failed, one more time"
            self.fetch_html()
            rank = self.soup.find('b', {'class': 'rank_text'})
            tries = tries - 1
          
        if rank is None:
            print "no rank"
            return "no rank"
        
        else:
            
            return rank.string
    
    def fetch_address(self): #every hotel has address, no exception
        
        '''fetch address'''
        ##print self.soup
        address =""
        tags = self.soup.find('span',{'rel':'v:address'})
        tries = 3
        while tags is None and tries > 0:
            
            print "address failed, one more time"
            self.fetch_html()
            tags = self.soup.find('span',{'rel':'v:address'})
            tries = tries - 1
        if tags is None:
            
            return "No Address"
        
        else:
            for tag in tags.findAll('span'):
                if tag.string is not None:
                    loc = tag.string.replace(',',' ')
                    address = address + " " + loc
            return address
    
        
    
    def fetch_total_reviews(self):  ##finish exception
        
        '''fetch total_reviews'''
        total_reviews = self.soup.find('span', {'property':'v:count'})
        tries = 2
        
        while total_reviews is None and tries > 0:
            print "total reviews failed, one more time"
            self.fetch_html()
            total_reviews = self.soup.find('span', {'property':'v:count'})
            tries = tries - 1
            
        if total_reviews is None :
            return '0'
        
        else:
            
            #result = ''.join(total_reviews.split(','))
            return total_reviews.string
    
    
    def fetch_sub_reviews(self, rev, i): ## finish exception 
        '''fetch sub reviews for different group'''
        values = "segment segment" + str(i)
        #print values
        tag = self.soup.find('div',{'class' : values})
        if tag is None: ##no subreview
            print "no sub review"
            self.fill_empty_review(rev, i)
        else:   ##there are subreivews
            count = tag.find('div', {'class' : 'value'}).string.replace(',','')
            ##sub total review
            rev.table[i].append(count)
            params = "?" + FetchInfo.segment_list[i-1] + "&returnTo=" + self.returnTo + "&filterRating=0"
            post_url = FetchInfo.post_url + params
            #print post_url
            request = requests.get(post_url)
            html = BeautifulSoup(request.content)
            datas = html.findAll('div',{'class' : 'wrap row'})
            if len(datas) == 0:
                    
                self.fill_empty_review(rev,i)
            else:
                
                for data in datas:
                    nums = data.find('span',{'class': 'compositeCount'}).string.replace(',','')
                    rev.table[i].append(nums)
            
    
    
    def fetch_rating(self,rev,index):   ##finish exception
        '''fetch rating'''
        
        summary_box = self.soup.find('div', {'id' : 'SUMMARYBOX'})
        if summary_box is None:
            self.fill_empty_summary(rev,index)
        else:
            tags = summary_box.findAll('img', {'class' : 'sprite-rating_s_fill'})
            if len(tags) == 6:
                for data in tags:
                    summary = data['alt'].split(' ')
                    rev.table[index].append(summary[0])
            else:
                self.fill_rating(summary_box,rev,index)
        
    
    def fetch_review_properties(self, rev, total, index): #finish exception
        '''build two demensions table'''
        
        if index == 0:
            
            rev.table[index].append(total.replace(',','')) #remove ',' in the total_review
            datas = self.soup.findAll('div',{'class' : 'wrap row'})
            if datas is None or len(datas) == 0:
                
                self.fill_empty_review(rev,index)
            else:
                
                for data in datas:
                    count = data.find('span',{'class': 'compositeCount'}).string
                    rev.table[index].append(count.replace(',',''))
        else:
            ##fetch information after click on families,Couples,Solo, Business
            self.fetch_sub_reviews(rev,index)
            
        self.fetch_rating(rev,index)
        
    def fill_empty_review(self,rev,i):
        
        j = 0
        while j < 6:
            rev.table[i].append("0")
            j = j + 1
            
    def fill_empty_summary(self,rev,i):
        j = 0
        while j < 6:
            rev.table[i].append("0")
            j = j + 1
            
    def fill_rating(self,summary_box,rev,index):
        dictionary = {"Location":'0',"Sleep Quality":'0',"Rooms": '0','Service':'0','Value':'0','Cleanliness':'0'}
        pos = ["Location","Sleep Quality","Rooms",'Service','Value','Cleanliness']
        for li in summary_box.findAll('li'):
            name = li.find('div',{'class':'name'}).string
            values = li.find('img')['alt'].split(' ')
            dictionary[name] = values[0]
            #print  name + dictionary[name]
        for key in pos:
            rev.table[index].append(dictionary[key])
'''manual start up'''
'''
url = "http://www.tripadvisor.com/Hotel_Review-g60763-d6877735-Reviews-Fairfield_Inn_New_York_Manhattan_Financial_District-New_York_City_New_York.html"
hotel_name = "Fairfield Inn New York Manhattan Financial District"
fetch = FetchInfo(url)
##fetch thumb_up rank and total_reviews
thumb_up = fetch.fetch_thumb_up() #thumb up
rank =  fetch.fetch_rank()  #rank
total_reviews = fetch.fetch_total_reviews()   #total_reviews
address = fetch.fetch_address()
rev  = Review(hotel_name,address,thumb_up,rank[8:]) #Review Object

##fill all review properties in the reviewers
i = 0
while i <= 4:
    
    fetch.fetch_review_properties(rev,total = total_reviews, index = i)
    i = i + 1       
#rev.write_into_file()


##write the table head into file
file_handle = open(Review.file_path,'w')
table_head = []
for data in Review.rows:
    table_head.append(str(data).center(15))
pad = "|"
table_head = pad.join(table_head) 
file_handle.write(table_head + '\n')
##write table lines into file

for attr in Review.cols:
    table_line= []
    table_line.append(attr.center(15))
    index = Review.cols.index(attr)
    for data in rev.table:
        if index < len(data) and data[index] is not None :
                   
            table_line.append(str(data[index]).center(15))
        else:
            table_line.append("##".center(15))
    table_line = pad.join(table_line)    
    file_handle.write(table_line + "\n")
file_handle.close()
print thumb_up
print rank
print address
##print "finish " + self.hotel_name + " !"      

'''





















