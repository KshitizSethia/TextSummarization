from similarity import text_similarity
from article import article
from tfidf import calculate_global_frequency
import math
import cPickle
import os
import matplotlib.pyplot as plt

def main():
    data_dir = "./data/data_4"
    calculate_global_frequency()
    countertotal = cPickle.load(open("idf.dat","rb"))

    x_axis = []
    y_axis_1 = []
    y_axis_2 = []
    y_axis_3 = []
    y_axis_4 = []
    y_axis_5 = []
    c = 1

    use_tfidf = 1

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

                        first_sentence_summary += " " + thisArticle.paras[para_index].split(".")[0]
                        if len(thisArticle.paras[para_index].split(".")) > 1:
                            second_sentence_summary += " " + thisArticle.paras[para_index].split(".")[1]
                            two_sentence_summary += " " + thisArticle.paras[para_index].split(".")[0] + " " + thisArticle.paras[para_index].split(".")[1]
                        full_article_summary += " " + thisArticle.paras[para_index]
                        
            #print first_sentence_summary
            #print actual_summary

                        
            #print first_sentence_summary
            #print actual_summary

            l_d = float(len(full_article_summary.split(" ")))
            l_fs = float(len(first_sentence_summary.split(" ")))
            l_ss = float(len(second_sentence_summary.split(" ")))
            l_ts = float(len(two_sentence_summary.split(" ")))
            l_as = float(len(actual_summary.split(" ")))

            x_axis.append(thisArticle.title)
            first_sentence_result = (text_similarity(first_sentence_summary, actual_summary, use_tfidf, countertotal)) - math.sqrt(max(0.0, ((l_fs - l_as)/(l_d - l_as))))
            second_sentence_result = (text_similarity(second_sentence_summary, actual_summary, use_tfidf, countertotal)) - math.sqrt(max(0.0, ((l_ss - l_as)/(l_d - l_as))))
            two_sentence_result = (text_similarity(two_sentence_summary, actual_summary, use_tfidf, countertotal)) - math.sqrt(max(0.0, ((l_ts - l_as)/(l_d - l_as))))
            full_article_result = (text_similarity(full_article_summary, actual_summary, use_tfidf, countertotal)) - math.sqrt(max(0.0, ((l_d - l_as)/(l_d - l_as))))
            avg_result = (first_sentence_result + two_sentence_result + second_sentence_result) / 3.0 ;

            #print thisArticle.title, '\t\t', avg_result, " l_fs ", l_fs, " l_as ", l_as, " l_d", l_d, " value ", math.sqrt(max(0.0, ((l_fs - l_as)/(l_d - l_as))))
            print thisArticle.title, '\t\t', avg_result
            
            if avg_result > 0.3:
                x_axis.append(thisArticle.title)
                y_axis_1.append(first_sentence_result)
                y_axis_2.append(second_sentence_result)
                y_axis_3.append(two_sentence_result)
                y_axis_4.append(full_article_result)
                y_axis_5.append(avg_result)
                

        except Exception as exp:
            #print filename
            print "\terror: " +str(exp)
    print x_axis
    print y_axis_1
    print y_axis_2
    print y_axis_3
    print y_axis_4
    print y_axis_5

    plt.plot(y_axis_1, label='first')
    plt.plot(y_axis_2, label='second')
    plt.plot(y_axis_3, label='two')
    plt.plot(y_axis_4, label='full')
    plt.plot(y_axis_5, label='average of 3')
    print len(y_axis_1)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
