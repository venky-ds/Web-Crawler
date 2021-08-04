import requests
import time
import pandas as pd
import random
from bs4 import BeautifulSoup
import csv
import logging

logging.basicConfig(level=logging.INFO, filename='sample.log')

#Function for downloading html pages using beautiful soup
def downloader(url):
  print("I am in downloader")
  logging.info(url)
  heads = {'Host': 'www.walmart.com', 'Connection': 'close',
         'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }
  for page_no in range(1,3):
    try:
      params ={'page':str(page_no),'sort':'submission-desc'}
      response = requests.get(url, headers=heads,params=params)
      logging.info("Downlading page no {page_no}".format(page_no=page_no))
      response.raise_for_status()
      soup = BeautifulSoup(response.content, 'html.parser')
      
      filename = f'{page_no}.html'
      with open(filename, "w", encoding = 'utf-8') as file:
        # prettify the soup object and convert it into a string  
        file.write(str(soup.prettify()))
      file.close()
      logging.info("File completed for"+str(page_no))
      time.sleep(random.randint(40,70))
    except Exception as e:
      print("Error")
      logging.critical("Error while downloading page"+str(page_no)+str(e))
    print("Downloaded page",page_no)
  logging.info("Download successfully over")

#Code for writing to csv file
def writer(rows):
  # field names 
  fields = [' Review date', 'Reviewer name', 'Review title', 'Review body','Rating'] 
  # name of csv file 
  filename = "walmart_output2.csv"
  log.info("Writing process beginning......")
 
  # writing to csv file 
  with open(filename, 'w',newline="") as csvfile: 
      # creating a csv writer object 
      csvwriter = csv.writer(csvfile) 
      # writing the fields 
      csvwriter.writerow(fields) 
      # writing the data rows 
      csvwriter.writerows(rows)
  logging.info("Writing process completed......")

#URL can be modified for specific product
url = 'https://www.walmart.com/reviews/product/14898365'
url2='https://www.walmart.com/ip/Gucci-Sync-XXL-White-Rubber-Unisex-Watch-YA137102/174437644'
#Function call for downloader
downloader(url2)
#Extracting required data from downloaded files. 
rows= []
for i in range(1,3):
  logging.info("Processing file "+str(i))
  root = r"C:\Users\venkyy\AppData\Local\Programs\Python\Python38\walmart2"
  file=f'{root}\{i}.html'
  
  #Parsing using Beautiful  Soup
  with open(file,encoding="utf8") as fp:
      soup = BeautifulSoup(fp, 'html.parser')
  fp.close()
  

  #Code to extract fields based on class name( Modified according to the retailer)
  reviews=soup.find_all("div", {"class": "Grid-col customer-review-body"})

  for item in reviews:
    title=''
    date=item.find("div", {"class": "review-date"}).span.text.strip()
    text=item.find("div", {"class": "review-text"}).text.strip()
    user=item.find("div", {"class": "review-user"}).span.text.strip()
    username= user.split()[-1]
    title_flag= item.find("h3", {"class": "review-title font-bold"})
    if title_flag:
      title=title_flag.text.strip()
    rating=item.find("div", {"class": "review-star-rating"})
    exact_rating=rating.find("span", {"class": "visuallyhidden seo-avg-rating"}).text.strip()
    rows.append([date,username,title,text,exact_rating])
  logging.info("Completed file "+str(i))


#Function call for writing
writer(rows)
  

  



  

  

  


  


