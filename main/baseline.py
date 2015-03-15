from similarity import text_similarity
from article import article
import cPickle
import os

def main():
    data_dir = "./data"
    #for filename in os.listdir(data_dir):
    try:
        path = r"C:\Cloud\github\TextSummarization\main\data\Finance.dat"#os.path.join(data_dir, filename)#"C:\\Cloud\\github\\TextSummarization\\main\\data\\87th_Academy_Awards.dat"#
        thisArticle = cPickle.load(open(path,"rb"))
        
        first_sentence_summary= ""
        actual_summary = ""
        for section_name in thisArticle.sections.keys():
            for para_index in thisArticle.sections[section_name]:
                if(section_name =="intro"):
                    actual_summary += thisArticle.paras[para_index]
                else:
                    first_sentence_summary += thisArticle.paras[para_index].split(".")[0]
                    
        #print first_sentence_summary
        #print actual_summary
        print text_similarity(first_sentence_summary, actual_summary)
    except Exception as exp:
        #print filename
        print "\terror: " +str(exp)

if __name__ == "__main__":
    main()