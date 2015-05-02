import cPickle
import os
import re
import sys

from article import article

# resources: pythex.org for regex testing
def main():
    verbose = False
    if("-v" in sys.argv):
        verbose=True

    dir_name = sys.argv[1]
    for file in os.listdir(dir_name):
        try:
            text = open(os.path.join(dir_name,file), "r").read()
            
            thisArticle = article()
            thisArticle.title = file
            
            thisArticle.paras = text.split("\n\n")
            
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
                print "---------------------END " + thisArticle.title + "---------------------"
             
            # cPickle.dump(inner_text_noRev, open(settings.raw_folder + title + ".txt", "wb"))
            cPickle.dump(thisArticle, open("./data/"+file+".dat", "wb"))
        except Exception as exp:
            print file
            print "details: " + str(exp)

if __name__ == "__main__":
    main()
