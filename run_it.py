#!python3
import requests
from bs4 import BeautifulSoup
import os
import sys

#turn it True if you also want to download books
download_books = True
mozilla_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
headers = {'User-Agent':mozilla_agent}
books_dir = os.path.dirname(os.path.abspath(__file__)) +'/download_books'
if download_books and not os.path.exists(books_dir):
    os.mkdir(books_dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
main_url = 'http://allitebooks.com'

infile=open(current_dir + '/links.txt','a')

r = requests.get(main_url,headers=headers)
page = 1
while page < 746:
    bsObj = BeautifulSoup(r.content, 'html.parser')
    a = bsObj.findAll('h2',{'class':'entry-title'})
    for n in a:
        inpage =requests.get(n.a['href'],headers=headers)
        try:
            book_title = n.a.get_text()
        except:
            book_title = 'not found'
        newbsObj = BeautifulSoup(inpage.content,'html.parser')
        try:
            download_link = newbsObj.find('span',{'class':'download-links'}).a['href']
            if download_books:
                try:
                    file_name= books_dir + '/' + download_link.split('/')[-1]
                    with open(file_name, 'wb') as f:
                        print("Downloading %s" % file_name)
                        response = requests.get(download_link, stream=True,headers=headers)
                        total_length = response.headers.get('content-length')
                        if total_length is None: #no content length header
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size=4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                                sys.stdout.flush()
                except:
                    pass
        except:
            download_link ='no download link found'
        try:
            author = newbsObj.find('div',{'class':'book-detail'}).dl.findAll('dd')[0].a.get_text()
        except:
            author = 'not found'
        try:
            size = newbsObj.find('div',{'class':'book-detail'}).dl.findAll('dd')[5].get_text()
        except:
            size = 'not found'
        try:
            category = newbsObj.find('div',{'class':'book-detail'}).dl.findAll('dd')[7].a.get_text()
        except:
            category = 'Technology'
        try:
            date = newbsObj.find('div',{'class':'book-detail'}).dl.findAll('dd')[2].get_text()
        except:
            date = 'not found'
        infile.write('{}\n{}\n{}\n{}\n{}\n{}'.format(book_title,download_link,author,size,category,date))
        try:
            print(newbsObj.find('span',{'class':'download-links'}).a['href'])
        except:
            print('love me like you do')
    shaka = main_url + '/page/' + str(page)
    print(shaka)
    page +=1
    r = requests.get(main_url +'/page/' + str(page))
    
