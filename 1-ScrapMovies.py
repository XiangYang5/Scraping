# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:17:55 2018

@author: Xiang Yang
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re,time,os,codecs
from bs4 import BeautifulSoup


#make browser
ua=UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
driver = webdriver.Chrome('chromedriver.exe',desired_capabilities=dcap,service_args=service_args)

all_movie = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'

driver.get(all_movie)

webLink = 'https://www.rottentomatoes.com'

movies = set()

#genre = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="genre-dropdown"]/div/div/div[1]/span')))
#genre.click()

for i in range (0,9):
    try:
        
        html=driver.page_source# get the html
        soup = BeautifulSoup(html, "lxml") # parse the html 
        all_movies=soup.findAll('div', {'class':re.compile('movie_info')}) # get all the review divs
        
        #print(all_movies)
        #print('*********************')
        for x in all_movies:
            link=x.find('a',{'href':re.compile('/m/')})
            movLink = webLink + str(link).split('"')[1]
            print(movLink)
            movies.add(str(movLink))    #creating the distinct list of movies
        
        #print(movies)
        showMoreButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="show-more-btn"]/button')))
        #click on the showMore Button
        showMoreButton.click()
        print('click: ',i)
    except:
        print ('missing show More button')
    
    
#writing the set entries to movie file
try:
    fw=open('movie_link.txt','w') # output file
    
    for x in movies:
        fw.write(x +"\n")
        
    fw.close()
except:
    print("Error while trying to create movie_link.txt file")
    




    
    