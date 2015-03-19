from similarity import text_similarity
from article import article
from tfidf import calculate_global_frequency

import cPickle
import os
import matplotlib.pyplot as plt

def main():
<<<<<<< HEAD
    data_dir = "./data/data_4"
    calculate_global_frequency()
    countertotal = cPickle.load(open("idf.dat","rb"))
=======
    data_dir = "./data"
>>>>>>> FETCH_HEAD
    x_axis = []
    y_axis_1 = []
    y_axis_2 = []
    y_axis_3 = []
    y_axis_4 = []
    c = 1
<<<<<<< HEAD
    use_tfidf = 0
=======
>>>>>>> FETCH_HEAD
    for filename in os.listdir(data_dir):
        try:
            #path = r"C:\Cloud\github\TextSummarization\main\data\Finance.dat"#os.path.join(data_dir, filename)#"C:\\Cloud\\github\\TextSummarization\\main\\data\\87th_Academy_Awards.dat"#
            path = os.path.join(data_dir, filename)#"C:\\Cloud\\github\\TextSummarization\\main\\data\\87th_Academy_Awards.dat"#
            thisArticle = cPickle.load(open(path,"rb"))
            
            first_sentence_summary= ""
            second_sentence_summary= ""
            two_sentence_summary= ""
            full_article_summary = ""
            actual_summary = ""
            for section_name in thisArticle.sections.keys():
                for para_index in thisArticle.sections[section_name]:
                    if(section_name =="intro"):
                        actual_summary += thisArticle.paras[para_index]
                    else:
<<<<<<< HEAD
                        first_sentence_summary += " " + thisArticle.paras[para_index].split(".")[0]
                        if len(thisArticle.paras[para_index].split(".")) > 1:
                            second_sentence_summary += " " + thisArticle.paras[para_index].split(".")[1]
                            two_sentence_summary += " " + thisArticle.paras[para_index].split(".")[0] + " " + thisArticle.paras[para_index].split(".")[1]
                        full_article_summary += " " + thisArticle.paras[para_index]
                        
            #print first_sentence_summary
            #print actual_summary
            print thisArticle.title, '\t\t', text_similarity(first_sentence_summary, actual_summary, use_tfidf, countertotal)
            x_axis.append(thisArticle.title)
            y_axis_1.append(text_similarity(first_sentence_summary, actual_summary, use_tfidf, countertotal))
            y_axis_2.append(text_similarity(second_sentence_summary, actual_summary, use_tfidf, countertotal))
            y_axis_3.append(text_similarity(two_sentence_summary, actual_summary, use_tfidf, countertotal))
            y_axis_4.append(text_similarity(full_article_summary, actual_summary, use_tfidf, countertotal))
=======
                        first_sentence_summary += thisArticle.paras[para_index].split(".")[0]
                        if len(thisArticle.paras[para_index].split(".")) > 1:
                            second_sentence_summary += thisArticle.paras[para_index].split(".")[1]
                            two_sentence_summary += thisArticle.paras[para_index].split(".")[0] +thisArticle.paras[para_index].split(".")[1]
                        full_article_summary += thisArticle.paras[para_index]
                        
            #print first_sentence_summary
            #print actual_summary
            print thisArticle.title, '\t\t', text_similarity(first_sentence_summary, actual_summary)
            x_axis.append(thisArticle.title)
            y_axis_1.append(text_similarity(first_sentence_summary, actual_summary))
            y_axis_2.append(text_similarity(second_sentence_summary, actual_summary))
            y_axis_3.append(text_similarity(two_sentence_summary, actual_summary))
            y_axis_4.append(text_similarity(full_article_summary, actual_summary))
>>>>>>> FETCH_HEAD
        except Exception as exp:
            #print filename
            print "\terror: " +str(exp)
    print x_axis
    print y_axis_1
    print y_axis_2
    print y_axis_3
    print y_axis_4
    plt.plot(y_axis_1, label='first')
    plt.plot(y_axis_2, label='second')
    plt.plot(y_axis_3, label='two')
    plt.plot(y_axis_4, label='full')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
