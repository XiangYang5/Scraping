# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:40:47 2018

@author: Xiang Yang
"""
"""This script is to scrap html file of each moive link we get from ScrapMoives"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re,time,os,codecs

#make browser
ua=UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
driver = webdriver.Chrome('chromedriver.exe',desired_capabilities=dcap,service_args=service_args)

file=open('movie_link.txt')
#iterating over every Movie
for movie in file:
    try:
        name = str(movie).strip().split('/')[-1]
        print(name)
        driver.get(movie)    #visiting each movie    
        with codecs.open('movieshtml/'+name+'.html', 'w',encoding='utf8') as fw:
            fw.write(driver.page_source)# write the thember to strip to remove the lin-change character
    except:
        print ('Exception in saving file -',movie)

file.close()

    