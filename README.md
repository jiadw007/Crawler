Crawler
=======

Python Crawler

Simple Crawler for http://www.tripadvisor.com/

Purpose:

    Fetch Reviews information for hotels in cities.

structure: 

    crawler.py   startup
        http://www.tripadvisor.com/Hotels?seen=0&sequence=1&geo=60763&requestingServlet=Hotels&refineForm=true&o=%s&rad=0&da                   teBumped=NONE
        This url to get hotel list
        geo:    city code
        o:  page number
    fetchInfo.py
        fetch all necessary info.
    review.py
        store the results and write to csv

Result:

    city.csv
         
         
Next step:

    Improve efficiency by multithreading (my idea).
         
    Good practice for multithreading.
    
