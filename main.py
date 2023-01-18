from bs4 import BeautifulSoup
import io
import requests
from progress.bar import IncrementalBar
import os.path

f = io.open(".\html.txt", mode="r", encoding="utf-8")
soup = BeautifulSoup(f, 'html.parser')

aname = []

i = 0

for group in soup.find_all('ul', {'class' : 'mainSongs'}):
    for name in group.find_all('span', {'class' : 'artist'}):
        aname.append(name.get_text())
    bar = IncrementalBar('Countdown', max = len(aname))
    for href in group.find_all('li', {'class' : 'play'}):
        bar.next()
        t = 2 
        while os.path.exists("in\\" + aname[i] + ".mp3"):
            if t < 10:
                aname[i] = aname[i][:-3] + "(" + str(t) + ")"
            else:
                if t <100:
                    aname[i] = aname[i][:-4] + "(" + str(t) + ")"
                else:
                    if t <1000:
                        aname[i] = aname[i][:-5] + "(" + str(t) + ")"
                    else:
                        aname[i] = aname[i][:-6] + "(" + str(t) + ")"
                
            t = t + 1
        
        p = requests.get(href['data-url'])
        if p.status_code != 200:
            print("Ошибка " + str(p.status_code) + " при скачивании фала " + aname[i])
            
        out = open("in\\" + aname[i] + ".mp3", "wb")
        out.write(p.content)
        out.close()
        
        i = i + 1
f.close()

print("Программа завершена")
