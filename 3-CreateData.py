# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 20:53:29 2018

@author: Xiang Yang
"""

from bs4 import BeautifulSoup
import re
import os

movieinfo=open('movieinfo.txt','w')
movie_info={}
files = os.listdir("C:/Users/stuar/Documents/BIA 660/movie_list")


  #get critics critics scores
def  getCriticScore(soup):
    criticChunk=soup.find('span',{'class':re.compile('meter-value')})
    if criticChunk: critic_score=criticChunk.text#.encode('ascii','ignore')
    movie_info["critic_score"]=critic_score
    return critic_score

 #get audiance scores
def  getAudianceScore(soup):
        audianceChunk=soup.find('div',{'class':("audience-score meter")})      
        if audianceChunk: audiance=audianceChunk.text.strip()
        audiance_score=str(audiance).split('\n')[0]#only keep score
        movie_info["audiance_score"]=audiance_score
        return audiance_score

      #get movie titles
def  getMovieTitle(soup):
    movietitlesChunk=soup.find("h1",{"id":("movie-title")})	
    if  movietitlesChunk: moviestitles= movietitlesChunk.text
    movies_titles=moviestitles.split('(')[0] #remove year
    moviestitles_1=movies_titles.strip() #remove spaces
    movie_info["movietitle"]=moviestitles_1
    
    #print(moviestitles_1)
    return moviestitles_1

#get critics info
def  getCriticInfo(soup):    
    info = []
    
    critics_average_rating ='NA'
    critics_reviews_counted = 'NA'
    critics_top ='NA'
    critics_fresh = 'NA'
    critics_rotten = 'NA'
    #get critics info
    
    try: 
        criticsChunk=soup.find('div',{'id':('scoreStats')})
        if criticsChunk:criticsinfo=criticsChunk.text.strip()
        criticsinfo_1=criticsinfo.split()
        
        #print(criticsinfo_1)
        critics_average_rating=criticsinfo_1[2]
        critics_reviews_counted=criticsinfo_1[5]
        critics_fresh=criticsinfo_1[7]
        critics_rotten=criticsinfo_1[9]
        
        all_critcsChunk=soup.find('p',{'id':('criticHeaders')})

        if all_critcsChunk: all_critics=all_critcsChunk.text.strip()
        all_critics_1=all_critics.split('|')
        top_critics=re.sub('[^0-9]',' ',all_critics_1[1].strip())
        critics_top=top_critics.strip()

    except:
        print("Error in getCriticInfo ")
        
    info.append(critics_average_rating)
    info.append(critics_reviews_counted)
    info.append(critics_top)
    info.append(critics_fresh)
    info.append(critics_rotten)
        
    
    #print(critics_average_rating,critics_reviews_counted,critics_fresh,critics_rotten) 
    return info

#get audiance info
def getAudienceInfo(soup):
    
    aud_info =[]
    audiance_average_rating ='NA'
    user_ratings ='NA'
    
    try:
        audianceinfoChunk=soup.find('div',{'class':('audience-info hidden-xs superPageFontColor')})
        if audianceinfoChunk: audianceinfo=audianceinfoChunk.text
        audianceinfo_1=audianceinfo.split()
        audiance_average_rating=audianceinfo_1[2]
        user_ratings=audianceinfo_1[5]
    
    except:
        print("Error in getAudienceInfo ")
    
    aud_info.append(audiance_average_rating)
    aud_info.append(user_ratings)
    
    return aud_info


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getMovieInfo(soup):
    try:
        movieInfoDict = {}
        rating ='NA'
        genre = 'NA'
        director ='NA'
        writter = 'NA'
        release_date ='NA'
        streaming_date ='NA'
        runtime= 'NA'
        box_office ='NA'
        studio ='NA'
        movieInfoChunk = soup.find('ul',{'class':'content-meta info'})
        for data in movieInfoChunk:
            x = cleanhtml(str(data)).strip()
            #print(x.strip())           
            if(len(x))>0:
                x= re.sub('\n','',x).strip()
                x = x.split(':')
                key = str(x[0])
                value = ''.join(x[1:]).strip()
                #print(key,'-----',value.strip())
                movieInfoDict[key]= value
        
        #print the dictionary
        #print(movieInfoDict)
        if 'Rating' in movieInfoDict : rating = movieInfoDict['Rating']
        if 'Genre' in movieInfoDict : 
            genre = re.sub('&amp;','&',movieInfoDict['Genre'])
            genre = genre.split(',')
            genre = [item.strip() for item in genre]
            genre = ','.join(genre)
        if 'Runtime' in movieInfoDict : runtime = movieInfoDict['Runtime']    
        if 'Directed By' in movieInfoDict : director = movieInfoDict['Directed By']
        if 'Written By' in movieInfoDict :  writter = movieInfoDict['Written By']
        if 'In Theaters' in movieInfoDict : release_date = movieInfoDict['In Theaters']
        if 'On Disc/Streaming' in movieInfoDict : streaming_date = movieInfoDict['On Disc/Streaming']
        if 'Box Office' in movieInfoDict : box_office = movieInfoDict['Box Office']
        if 'Studio' in movieInfoDict : studio = movieInfoDict['Studio']
         
    except:
        print('Error Parsing Movie ')
    
    info = []
    info.append(rating)
    info.append(genre) 
    info.append(director) 
    info.append(writter) 
    info.append(release_date) 
    info.append(streaming_date)
    info.append(runtime)
    info.append(box_office)
    info.append(studio)     
    return info

def getCast(soup):
    castList = []
    
    castChunk = soup.find('div',{'class':'castSection'})
    #print(len(castChunk))
    try:
        for cast in castChunk:
            cast = cleanhtml(str(cast)).strip()
            #print(cast)
            #print('```````````````````````````````````````')
            cast = cast.split("\n")[0]
            #print(cast)
            if len(str(cast)) > 1 : castList.append(str(cast))
            #print('***********************************')
        castList = castList[:-2]
        #print(castList)
    except:
        print('exception in getCast block')
    
    return (castList)   
    
totallist=['movietitle','critic_score', 'audiance_score', 'critics_average_rating', 'critics_reviews_counted','critics_top', 'critics_fresh', 'critics_rotten', 'audiance_average_rating', 'user_ratings']


fw=open('Web_Data.txt','w') # output file

fw.write('movietitle'+'\t'+'critic_score'+'\t'+ 'audiance_score'+'\t'+ 'critics_average_rating'+'\t'+ 'critics_reviews_counted'+'\t'+ 'critics_top'+'\t'+'critics_fresh'+'\t'+ 'critics_rotten'+'\t'+ 
         'audiance_average_rating'+'\t'+
         'user_ratings'+'\t'+
         'rating'+'\t'+
        'genre'+'\t'+ 
        'director' +'\t'+
        'writter'+'\t'+ 
        'release_date'+'\t'+ 
        'streaming_date' +'\t'+ 
        'runtime' +'\t'+ 
        'box_office'+'\t'+ 
        'studio'+'\t'+
        'cast'+'\t'+
        'top5Cast'+
        '\n')

for file in files:
    if file.endswith('html'):
        title ='NA'
        critic_score ='NA'
        audiance_score='NA'
        critics_average_rating ='NA'
        critics_reviews_counted ='NA'
        critics_top ='NA'
        critics_fresh ='NA'
        critics_rotten ='NA'
        audiance_average_rating ='NA'
        user_ratings ='NA'
        rating ='NA'
        genre = 'NA'
        director ='NA'
        writter = 'NA'
        release_date ='NA'
        streaming_date ='NA'
        runtime= 'NA'
        box_office ='NA'
        studio ='NA'
        cast ='NA'
        top5cast ='NA'
        
        try:
            movie_data=[]
            
            soup = BeautifulSoup(open(file), "html.parser")
            #print('Reading Each File')
            
            title = getMovieTitle(soup)
            movie_data.append(title)
            
            critic_score = getCriticScore(soup)
            movie_data.append(critic_score)
            
            audiance_score = getAudianceScore(soup)
            movie_data.append(audiance_score)
            
            critic_info = getCriticInfo(soup) # returns a list
            
            movie_data.append(critic_info[0])
            movie_data.append(critic_info[1])
            movie_data.append(critic_info[2])
            movie_data.append(critic_info[3])
            movie_data.append(critic_info[4])
            
            critics_average_rating =critic_info[0]
            critics_reviews_counted =critic_info[1]
            critics_top = critic_info[2]
            critics_fresh =critic_info[3]
            critics_rotten =critic_info[4]
            
            aud_info = getAudienceInfo(soup)
            
            movie_data.append(aud_info[0])
            movie_data.append(aud_info[1])
            
            audiance_average_rating =aud_info[0]
            user_ratings =aud_info[1]
            
            
            info = getMovieInfo(soup)
            
            rating =info[0]
            genre = info[1]
            
            director =info[2]
            writter = info[3]
            release_date =info[4]
            streaming_date =info[5]
            runtime= info[6]
            box_office =info[7]
            studio =info[8]
            
            cast = getCast(soup)
            top5cast = cast[0:5]
            
            cast = ','.join(cast)
            top5cast = ','.join(top5cast)
            totallist.append(movie_data)
        
        except:
            print('Error trying to parse data')
        
        try:
            #print(title)
            #print(user_ratings)
            fw.write(title +'\t'+ critic_score +'\t'+
                        audiance_score+'\t'+
                        critics_average_rating +'\t'+
                        critics_reviews_counted +'\t'+
                        critics_top +'\t'+
                        critics_fresh +'\t'+
                        critics_rotten +'\t'+
                        audiance_average_rating +'\t'+
                        user_ratings +'\t'+
                        rating +'\t'+
                        genre +'\t'+
                        director +'\t'+
                        writter +'\t'+
                        release_date +'\t'+
                        streaming_date +'\t'+
                        runtime +'\t'+
                        box_office +'\t'+
                        studio +'\t'+
                        cast+'\t'+
                        top5cast +'\n')
        except:
             print('Error trying to write data')

fw.close()
print('complete writing')

'''
myFile = open('movieinfo.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(totallist)
     
print("Writing complete")
'''
