# IPython log file

get_ipython().magic(u'logstart C:\\Cloud\\github\\TextSummarization\\downloader\\main2.py')
import os
os.chdir("C:\Cloud\github\TextSummarization\downloader\")
os.chdir("C:\Cloud\github\TextSummarization\downloader")
os.getcwd()
from bs4 import BeautifulSoup
import urllib2
html_raw = urllib2.open("http://en.wikipedia.org/wiki/Percival_Thirlwall").read()
html_raw = urllib2.urlopen("http://en.wikipedia.org/wiki/Percival_Thirlwall").read()
html_raw
html_parsed = BeautifulSoup(html_raw)
print soup.get_text()
print html_parsed.get_text()
print html_raw
html_raw.encode('ascii', 'ignore')
str(html_parsed)
paras = html_parsed.find('p')
for para in paras:
    print para
    ("")

for para in paras:
    print "*****" +para

for para in paras:
    print "*****" +para.string

print html_parsed.prettify()
html_parsed = BeautifulSoup(urllib2.urlopen("http://en.wikipedia.org/wiki/Percival_Thirlwall").read().decode("utf-8"))
print html_parsed.prettify()
html_parsed = BeautifulSoup(urllib2.urlopen("http://en.wikipedia.org/wiki/Percival_Thirlwall").read().decode("utf8"))
print html_parsed.prettify()
h2s = html_parsed.find("h2")
for h2 in h2s:
    print h2.text()
    print "**end"

for h2 in h2s:
    print h2

for h2 in h2s:
    print "**end"
    print h2

print html_parsed.body.p
print html_parsed.body.p[1]
for para in html_parsed.body.p:
    print para

for para in html_parsed.find_all('p'):
    print "para:  "
    print para

for para in html_parsed.find_all('p'):
    print "para:  "
    print para.text()

for para in html_parsed.find_all('p'):
    print "para:  "
    print para.p

for para in html_parsed.find_all('p'):
    print "para: "
    print BeautifulSoup(para).get_text()

html_parsed = BeautifulSoup(urllib2.urlopen("http://en.wikipedia.org/w/index.php?title=Percival_Thirlwall&action=edit").read().decode("utf-8"))
print html_parsed.textarea
print html_parsed.textarea.string
type(html_parsed.textarea)
