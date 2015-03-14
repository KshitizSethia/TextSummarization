from bs4 import BeautifulSoup
import urllib2
import re
import cPickle
import sys

from article import article

#resources: pythex.org for regex testing

def main():
    titles = open("title_list.csv", "r").read().split(',')

    for title in titles:
        try:
            uri = "http://en.wikipedia.org/w/index.php?title="+title+"&action=edit"
            html_parsed = BeautifulSoup(urllib2.urlopen(uri).read().decode("utf8"))
            
            thisArticle = article()
            
            inner_text = html_parsed.textarea.string
            inner_text_noRev = re.sub("{{.*?}}", "", inner_text)
            thisArticle.linked_titles = re.findall("\[\[(.*?)\]\]", inner_text_noRev)
            thisArticle.categories=re.findall("\[\[Category:(.*?)\]\]", inner_text_noRev)
            inner_text_cleaned = re.sub("\[\[(.*?)\]\]", r"\1", inner_text_noRev)
            inner_text_cleaned = inner_text_cleaned.encode('ascii', 'ignore')
            inner_text_cleaned = inner_text_cleaned.strip();
            
            thisArticle.paras = inner_text_cleaned.split("\n\n")
            
            section_splitter = re.compile("==(?P<section_name>.*?)==(?P<section_text>.*)")
            
            #todo find a better way to remove infobox
            if(thisArticle.paras[0].startswith("{{Infobox")):
                thisArticle.paras.pop(0)
        
            
            current_section = "intro"
            for index in range(len(thisArticle.paras)):
                thisArticle.paras[index] = thisArticle.paras[index].strip()
                
                
                match = re.match(section_splitter, thisArticle.paras[index])
                if(match):
                    current_section = match.group("section_name")
                    thisArticle.paras[index] = match.group("section_text")
                if(not current_section in thisArticle.sections.keys()):
                    thisArticle.sections[current_section] = []
                thisArticle.sections[current_section].append(index)
                
            cPickle.dump(inner_text_noRev, open("./raw/"+title+".txt", "w+"))
            cPickle.dump(thisArticle, open("../data/"+title+".dat", "w+"))
        except:
            print title

if __name__ == "__main__":
    main()
