import m3u8
import requests
from sys import platform
from os import system
import os
from multiprocessing.pool import ThreadPool
import shutil
from glob import glob

class RequestsClient():
    def download(self, uri, timeout=None, headers={}, verify_ssl=True):
        o = requests.get(uri, timeout=timeout, headers=headers)
        return o.text, o.url


def links(url):
    playlist = m3u8.load(url, http_client=RequestsClient())
    data = playlist.dumps()
    word = 'EXT-X-STREAM-INF'
    list = data.split(word)
    urls = []
    for i in range(1,len(list)):
        print(str(i) + ' || ' + list[i].split(',')[-1].split('\n')[0] + ' : ' + url.replace(url.split('/')[-1],list[i].split('=')[-1].replace('m3u8\n','m3u8').split('\n')[-1].replace('#','')))
        urls.append(url.replace(url.split('/')[-1],list[i].split('=')[-1].replace('m3u8\n','m3u8').split('\n')[-1].replace('#','')))
    return urls
 
def merg(f):
    print('Merging The Files')
    d = 'ts\\'
    files = open('tmp.txt','r',encoding = 'utf-8').readlines()
    m = files[0].split('/')[-1].replace("\n","")
    w = open(m,'wb')
    for i in range(1,len(files)):
        f = open(d + files[i].split('/')[-1].replace("\n",""),'rb')
        shutil.copyfileobj(f,w)
    w.close()
    print('[+] done')
     
def download(url):
    path = 'ts\\'
    file = url.split('/')[-1].replace('\n','')
    #print(file + ' download ',end = '')
    r = requests.get(url.replace('\n',''))
    w = open(path + file.replace('\n',''),'wb')
    w.write(r.content)
    w.close()
    return file

        
        
def ts(url):
    playlist = m3u8.load(url, http_client=RequestsClient())
    links = playlist.dumps()
    links = links.split('\n')
    file = 'tmp.txt'
    w = open(file,'w',encoding = 'utf-8')
    w.write('')
    w.close()
    for line in links:
        if line != '' and line[0] != '#':
            w = open(file,'a',encoding = 'utf-8')
            w.write(url.replace(url.split('/')[-1],line + '\n'))
            w.close()
            
    f = open(file,'r',encoding = 'utf-8').readlines()
    try:
     print('Total File To Download : ' + str(len(f)))
     if not os.path.exists('ts'):
        system('mkdir ts')
     results = ThreadPool(5).imap_unordered(download, f)
     for r in results:
        print(r + ' downloaded')
     merg(f)
     print('cleaning....')
     if platform == 'win32':
        system('del tmp.txt' )
        system('rmdir /Q /S ts')
     elif platform == 'linux':
        system('rm tmp.txt')
        system('rm ts -rf')
     print('[+] Done')

    except:
        print("Something went wrong...")

def options():
 while True:
    try:
        num = int(input('Select url : '))
        int(num)
        if num < 1 and num > len(urls):
            print('Please select from options')
        else:
            video = urls[num - 1]
            print(video)
            ts(video)
            break
    except ValueError:
        print('Please enter only number')
    
url = str(input("url : "))
urls = links(url)
an = str(input('Want to download file(Y/N) : '))
if an == 'Y' or an =='y':
    options()
else:
    print('Exiting....')

