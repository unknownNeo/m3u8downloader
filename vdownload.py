import m3u8
import requests
from sys import platform
from os import system
import os
from multiprocessing.pool import ThreadPool
import shutil
from tqdm import tqdm


class RequestsClient():
    def download(self, uri, timeout=None, headers={}, verify_ssl=True):
        o = requests.get(uri, timeout=timeout, headers=headers)
        return o.text, o.url

def links(url):
    urls = []
    playlist = m3u8.load(url, http_client=RequestsClient())
    for i in playlist.playlists:
        print('[Resolution : ' + str(i.stream_info.resolution[0]) + 'x' + str(i.stream_info.resolution[-1]) + '] : ' + url.replace(url.split('/')[-1],str(i.uri)))
        urls.append(url.replace(url.split('/')[-1],str(i.uri)))
    return urls
 
def check(url):
    playlist = m3u8.load(url, http_client=RequestsClient())
    return playlist.is_variant
    
def merg(f):
    print('Merging The Files')
    if platform == 'win32':
        d = 'ts\\'
    elif platform == 'linux':
        d = 'ts/'
    files = open('tmp.txt','r',encoding = 'utf-8').readlines()
    m = files[0].split('/')[-1].replace("\n","")
    w = open(m,'wb')
    for i in range(1,len(files)):
        f = open(d + files[i].split('/')[-1].replace("\n",""),'rb')
        shutil.copyfileobj(f,w)
    w.close()
    print('File : ' + files[i].split('/')[-1].replace("\n",""))
    print('[+] done')
     
def download(url):
    if platform == 'win32':
        path = 'ts\\'
    elif platform == 'linux':
        path = 'ts/'
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
     for _ in tqdm(ThreadPool(6).imap_unordered(download, f),total = len(f)):
         pass
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
        print('Cleaning....')
        if platform == 'win32':
            system('del tmp.txt' )
            system('rmdir /Q /S ts')
        elif platform == 'linux':
            system('rm tmp.txt')
            system('rm ts -rf')
        print("[+] Done")
    
     
def options():
 while True:
    try:
        num = int(input('Select url : '))
        int(num)
        if num < 1 and num > len(urls):
            print('[!]Please select from options')
        else:
            video = urls[num - 1]
            print(video)
            ts(video)
            break
    except ValueError:
        print('[!]Please enter only number')
    except KeyboardInterrupt:
        print('Exiting....')
        break
    
url = str(input("url : "))
if check(url):
    urls = links(url)
    options()
else:
    op = str(input('Want to Download the Link? (y/n) : '))
    if op == 'y' or op == 'Y':
        ts(url)
    

