import os
from fetchInfo import FetchInfo
from review import Review
import requests

from bs4 import BeautifulSoup

count = 150
page = 5
total_hotels = 451
base_url = "http://www.tripadvisor.com/"
#html_url = "Hotels-g60763-New_York_City_New_York-Hotels.html"
##write the csv head
'''
file_handle = open('D:\\Reviews\\new york.csv','w')
csv_line = "Name,Address,Thumb_up,Rank,"
for row in Review.rows:
    for col in Review.cols:
        section = col + "_" + row + ","
        csv_line = csv_line + section
file_handle.write(csv_line + "\n")
file_handle.close()
'''
try:
    while count < total_hotels:
        
        pad = "a" + str(30 * page)
        hotel_list_url = '''http://www.tripadvisor.com/Hotels?\
                                    seen=0&sequence=1&geo=60763&requestingServlet=Hotels&refineForm=true&o=%s&rad=0&dateBumped=NONE''' % pad
        html = requests.get(hotel_list_url).content
        soup = BeautifulSoup(html)        
        if page == 0:
            stats = soup.find('div',{'class':'slim_ranking'}).string.split(' ')
            for data in stats:
                if data == 'of':
                    index = stats.index(data)
                    total_hotels = int(stats[index + 1])
                    print total_hotels
                    break;
            
        for hotel in soup.findAll('a',{'class': 'property_title'}):
            hotel_name = hotel.string[1:]
            url_path = base_url + hotel['href']
            ##Initialize
            fetch = FetchInfo(url_path)
            ##fetch thumb_up rank and total_reviews
            thumb_up = fetch.fetch_thumb_up() #thumb up
            print thumb_up
            rank =  fetch.fetch_rank()  #rank
            total_reviews = fetch.fetch_total_reviews()   #total_reviews
            address = fetch.fetch_address()
    
            ##construct Review object       
            ##txt_title = """%s, %s, %s, %s """ %(hotel_name, thumb_up.string, rank.string, str(total_reviews) + " Reviews") # txt_title  
            rev  = Review(hotel_name,address,thumb_up,rank[8:]) #Review Object

            ##fill all review properties in the reviewers
            i = 0
            while i <= 4:
    
                fetch.fetch_review_properties(rev,total = total_reviews, index = i)
                i = i + 1       
            rev.write_into_file()
            count = count + 1
            print "No. " + str(count) + " finish " + rev.hotel_name + "!"
        page = page + 1
    
except Exception, e:
    print e
    print "finish all possible hotel"




    
    
