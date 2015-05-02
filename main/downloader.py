from bs4 import BeautifulSoup
import urllib2
import re
import cPickle
import shutil
import os

from article import article
import settings
import sys
# resources: pythex.org for regex testing


def main():
    verbose = False
    if('-v' in sys.argv): verbose = True
    
    shutil.rmtree(settings.raw_folder, ignore_errors=True)
    shutil.rmtree(settings.data_folder, ignore_errors=True)
    
    titles = open("title_list.csv", "r").read().split(',')
    os.makedirs(settings.raw_folder)
    os.makedirs(settings.data_folder)

    # #TODO take all titles
    for title in titles[0:100]:
        try:
            uri = "http://en.wikipedia.org/w/index.php?title=" + title + "&action=edit"
            html_parsed = BeautifulSoup(urllib2.urlopen(uri).read().decode("utf8"))
            
            
            thisArticle = article()
            thisArticle.title = title
            
            inner_text = html_parsed.textarea.string
            inner_text = inner_text.encode('ascii', 'ignore')
            rawFile = open(settings.raw_folder + title + ".txt", "w")
            rawFile.write(inner_text)
            
            inner_text_noRev = re.sub("{{(.|\n)*?}}", "", inner_text)
            thisArticle.linked_titles = re.findall("\[\[(.*?)\]\]", inner_text_noRev)
            thisArticle.categories = re.findall("\[\[Category:(.*?)\]\]", inner_text_noRev)
            inner_text_cleaned = re.sub("\[\[(.*?)\]\]", r"\1", inner_text_noRev)
            # remove <ref>*</ref> tags and <ref * /> tags
            inner_text_cleaned = re.sub("<ref>(.|\n)*?</ref> | <ref (.|\n)*/>", "", inner_text_cleaned)
            # inner_text_cleaned
            inner_text_cleaned = inner_text_cleaned.strip();
            
            
            thisArticle.paras = inner_text_cleaned.split("\n\n")
            
            # remove paragraphs with tables and infobox in them, not informative 
            thisArticle.paras = filter(lambda x: x.find("wikitable") < 0, thisArticle.paras)
            thisArticle.paras = filter(lambda x: not x.startswith("{{Infobox"), thisArticle.paras)
            
            # remove empty paragraphs
            thisArticle.paras = [para for para in thisArticle.paras if para.strip() != ""]
            
            section_splitter = re.compile("==[=]*(?P<section_name>.*?)[=]*==(?P<section_text>.*)")
            
            unwanted_sections = ["References", "See also", "Notes", "Notes and references", \
                                 "Further reading", "External links", "Works", "Publications", \
                                 "Discography", "Bibliography" ]
            
            current_section = "intro"
            index_FirstUnwantedSection = len(thisArticle.paras)
            for index in range(len(thisArticle.paras)):
                thisArticle.paras[index] = thisArticle.paras[index].strip()
                
                
                match = re.match(section_splitter, thisArticle.paras[index])
                if(match):
                    current_section = match.group("section_name")
                    if(current_section in unwanted_sections):
                        index_FirstUnwantedSection = index
                        break
                    thisArticle.paras[index] = match.group("section_text")
                if(not current_section in thisArticle.sections.keys()):
                    thisArticle.sections[current_section] = []
                thisArticle.sections[current_section].append(index)
            
            parasToRemove = range(index_FirstUnwantedSection, len(thisArticle.paras))
            parasToRemove.reverse()
            for index in parasToRemove:
               thisArticle.paras.pop(index)
               
            if(verbose):
                print "---------------------START " + thisArticle.title + "---------------------"
                for para in thisArticle.paras:
                    print para
                print inner_text_cleaned
                print "---------------------END " + thisArticle.title + "---------------------"
             
            # cPickle.dump(inner_text_noRev, open(settings.raw_folder + title + ".txt", "wb"))
            cPickle.dump(thisArticle, open(settings.data_folder + title + ".dat", "wb"))
        except Exception as exp:
            print title
            print "details: " + str(exp)

if __name__ == "__main__":
    main()
