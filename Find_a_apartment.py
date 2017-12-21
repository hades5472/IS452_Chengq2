import requests
import time

from bs4 import BeautifulSoup


class apart:
    def __init__(self,price,name,mj,type,hezu):
        self.price = price
        self.name = name
        self.mj = mj
        self.type = type
        self.hezu = hezu
class getinfo:
    def __init__(self,city):
        self.or_url = "http://"+city+'.58.com/pinpaigongyu/'
        self.url = "http://"+city+'.58.com/pinpaigongyu/'
        self.page = 1
        self.end = 1
        self.apalist = []
        while self.end:
            self.get_info()
            # self.check_end()
            self.nextpage()
            # self.end -= 0.25
        # self.html
    def get_info(self):
        temphtml = requests.get(self.or_url)
        content = temphtml.text
        soup = BeautifulSoup(content, 'html.parser')
        if len(soup.findAll("div", class_='tip')) > 0:
            self.end = 0
        else:
            for i in range(len(soup.findAll("div",class_ = 'des'))):
                a = soup.findAll("div",class_ = 'des')[i]
                b = soup.findAll("div",class_ = "money")[i].span
                sb = str(b)
                sa = str(a)
                sc = str(a)
                startb = sb.find('<b>')
                endb = sb.find('</b>')
                starta = sa.find('<p class="room">')
                enda = sa.find("</p >")
                startc = sc.find('<h2>')
                endc = sc.find('</h2>')
                newc = sc[startc+4:endc]
                lc = newc.split()
                place = '' + lc[1].split('(')[0]
                newa = sa[starta+16:enda]
                lb = sb[startb+3:endb].split('-')[0]
                la = newa.split()
                tempapa = apart(lb,place,la[1],la[0],lc[0])
                self.apalist.append(tempapa)
    def nextpage(self):
        self.page += 1
        self.suffix = "pn/"+str(self.page)+'/'
        self.or_url = self.url + self.suffix
        print(self.page)
        # In order to reduce the burden of the server. We set a sleep here and
        # in this way we will not be blocked
        # I have been blocked many times and can only crawl 20 pages of data
        time.sleep(20)
    # def check_end(self):
    #     pass
class filter:
    def __init__(self,apalist):
        self.apalist = apalist
    def byprice(self,low,high):
        templ = []
        for apa in self.apalist:
            if int(apa.price) > low and int(apa.price) < high:
                templ.append(apa)
        self.apalist = templ
    def bymj(self,low,high):
        templ = []
        for apa in self.apalist:
            tempmj = int(apa.mj.split('m')[0])
            if tempmj > low and tempmj < high:
                templ.append(apa)
        self.apalist = templ

# Here we type in the code of the city. 'bj' stand for the city Beijing
# If we want to find the apartments in Shanghai, the only thing we have to do is type in 'sh'

test = getinfo("bj")
print(test.apalist)
f = open('bj_apa.txt','w')
for apa in test.apalist:
    f.writelines(apa.name)
    f.writelines(' ')
    f.writelines(apa.hezu)
    f.writelines(' ')
    f.writelines(apa.price)
    f.writelines(' ')
    f.writelines(apa.mj)
    f.writelines(' ')
    f.writelines(apa.type)
    f.writelines('\n')
f.close()

# testcase:
# This is a filter I set for myself (20,50) means the area of my leasing apartment should be bigger the 30 square meter
# and no bigger than 50 square meters
wanttedapa = filter(test.apalist)
wanttedapa.bymj(30,50)

# It is the budget filter, I want it to be in the range of 3000RMB to 5000RMB
wanttedapa.byprice(3000,6000)
fn = open("bj_suitable_apa.txt",'w')
for apa in wanttedapa.apalist:
    fn.writelines(apa.name)
    fn.writelines(' ')
    fn.writelines(apa.hezu)
    fn.writelines(' ')
    fn.writelines(apa.price)
    fn.writelines(' ')
    fn.writelines(apa.mj)
    fn.writelines(' ')
    fn.writelines(apa.type)
    fn.writelines('\n')
fn.close()
# html = requests.get(test.url)
# print(html.text)