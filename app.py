import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
import time
import zipfile, shutil, io

def damit(text):
    return text.replace(' ','%20')

def damit_back(text):
    return text.replace('%20',' ')


class API(object):

    def __init__(self,series):
        self.main_url = 'http://www.tvsubtitles.net'
        self.url = 'http://www.tvsubtitles.net/search.php?q='
        self.regex = re.compile(r'<a href="/tvshow-(.*)')
        self.series = series
        self.res = {}
        self.lang = 'en'
        self.req = requests.get(self.url + self.series)
        self.soup = BeautifulSoup((self.req).text,"html.parser")


    def save_some(self,url):
        headers = {'Content-Type': 'application/zip'}
        response = requests.get(url, headers=headers)
        print response.status_code
        with open(damit_back(response.url).split('/')[-1], 'wb') as handle:
            try:
                if not response.ok:
                    print 'Error Shits'

                for block in response.iter_content(1024):
                    handle.write(block)
            except Exception as e:
                print e

    def save(self,url,name):
        r = requests.get(url, stream=True)
        with open(name, "wb") as code:
            code.write(r.content)
    def get_serial(self):
        for i in self.soup.find_all('a'):
            if self.regex.search(str(i)):
                self.res[i.get_text()] = [i.get_text() , int(''.join(re.findall(r'\d+',i['href'])))]
        for i in self.res:
            print i
        return self.res
        
        
    def select(self):
        c = self.get_serial()
        select = input('Select one :')
        this_series = ''.join([j for i,j in enumerate(c) if i == select])
        print "You've selected %s"%this_series
        return c[this_series]

    def get_season(self):
        c = self.select()
        self.req = requests.get(self.main_url + '/tvshow-' + str(c[1]) + '.html')
        self.soup = BeautifulSoup((self.req).text,"html.parser")
        seasons = self.soup.find('p',{'class':'description'}).text
        print seasons
        select = input('Select season :')
        chosen = str(''.join(re.findall(r'\d+',''.join([ i for i in seasons.split(' | ') if str(select) in str(i)]))))
        if chosen:
            this_season = self.main_url + '/download-' + str(c[1]) + '-' + chosen + '-' + self.lang + '.html'
            name = str('S'+ chosen)
        try:
            self.save_some(this_season)
            print this_season
            return 'Hola Amigo........'
        except Exception as e:
            print e
            return 'Bull SHits........'
        
        
        
if __name__ == '__main__':
    x = API(damit('person of interest'))
    print x.get_season()
    
