# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 2017

@author: Alexander Singleton 
"""

import time 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import os 

from collections import Counter
from wordcloud import WordCloud
###############################################################################

def top_N(dir_path, n):
    """Finds top n occurrences of words in any documents""" 
    
   # These sets remove special characters that may interfere with regex search    
    chars_to_remove = set(("^", "+", "?", "(",  ")", "{", "!",
                "}", "|", "[" ,"]", ">", "\\", "<", ".", ",", ";", "-", "\"" )) 
    
    chars_to_remove_less_stops = set(("^", "+", "(",  ")", "{",
                "}", "|", "[" ,"]", ">", "\\", "<", ",", ";", "-", "\"" ))             
    
    #These lists are to remove periods from common abbreviations 
    abbrev_List = [" U.S. ", " Mr. ", " Mrs. ", " Ms. ", " Dr. "]
    rep_List = [ " United States "," Mr ", " Mrs ", " Miss ", " Dr "]
    
    # Initialize variables
    directory_in_str = dir_path
    top_Blank = int(n)
    all_Raw_Sens = []
    all_Cln_Sens = []
    all_Words = []
    
    directory = os.fsencode(directory_in_str)
    docs_len = len(os.listdir(directory))                        
        
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): 
     
            found_File = open(os.path.join(directory_in_str, filename), 
                                                              encoding='utf8')
            search_Str = found_File.read()
            
            # Removes all punctuation, adds all words to a list
            cleaned_Text =  [c for c in search_Str if c 
                                               not in chars_to_remove]
            found_Text = ''.join(cleaned_Text)
            lower_Text = found_Text.lower()
            words = lower_Text.split()
            all_Words.extend(words)        
            
            # This loop prevents periods from common abbreviations like 'U.S.' 
            # from being split like real sentences
            for i in range(0, len(abbrev_List)):
                search_Str = search_Str.replace(abbrev_List[i], rep_List[i])
                           
            quest_Find = "(\? .)" 
            excl_Find = "(\! .)"
            per_Find = "(\. .)"
            
            regex = re.compile(quest_Find + "|" + excl_Find + "|" +  per_Find)  
            
            # Implements above regex. Removes grammatically incorrect stops.             
            i = 0; output = ""
            for m in regex.finditer(search_Str):
                
                if search_Str[m.end()-1] == search_Str[m.end()-1].lower():
                    output += "".join([search_Str[i:m.start()], 
                                            search_Str[(m.start()+1):m.end()]])
            
                else:
                   output += "".join([search_Str[i:m.end()]])         
                    
                i = m.end()                       
            search_Str = "".join([output, search_Str[m.end():]])
            
            # Splits sentences at all stops, keeps all other punctuation
            sentences = list((filter(None, re.split("[.?!]+", search_Str))))
            all_Raw_Sens.append(sentences)
            
            # Splits sentences at all stops, removes all other punctuation
            clean_Sentences = [c for c in search_Str if c 
                                             not in chars_to_remove_less_stops]
            found_Text_2 = ''.join(clean_Sentences)
    
            cln_Sentences = list((filter(None, re.split("[.?!]+", 
                                                               found_Text_2))))
            all_Cln_Sens.append(cln_Sentences)
                    
    if(len(all_Words) < top_Blank): 
        return(False)                
        
    # Magic one liner: Counts all unique words and their frequencies 
    common_Dict = Counter(all_Words).most_common(top_Blank)
               
    word = list(zip(*common_Dict))[0]
    word_List = []
    for com_word in word:
        word_List.append(com_word)  
    
    return (common_Dict, all_Words, docs_len, 
                                   all_Cln_Sens, all_Raw_Sens, word, word_List)    
############################################################################### 

def plot_Words(com_word, common_Dict, all_words):
    """Data Visualization of top n most common words in docs"""
             
    freq = list(zip(*common_Dict))[1]
    x_pos = np.arange(len(common_Dict)) 
       
    plt.bar(x_pos, freq, align='center')
    plt.xticks(x_pos, com_word) 
    plt.title('Plot of Most Common Words')
    plt.show()

# Generates WordCloud for visualizing data      
    words_For_Cloud = ' '.join(word for word in all_words)
    wordcloud = WordCloud(stopwords = '', 
                            max_words=len(com_word)).generate(words_For_Cloud)
    ## Generate plot
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
###############################################################################
def sentences(com_word, docs_len, cln_sens, raw_sens):   
    """Searches sentences for presence of the ith common word"""    
   
    all_Words_Sens = []
    word_Presence = []
                                    
    for common_Word in com_word:   #Common Word Level 
        found_In_Doc = []
        word_Sens_Alldocs = []
    
        for i in range(0, docs_len):  #Doc level
            doc_Found_Sens = []
            doc_Presence = False 
            
            text = re.compile(" " + common_Word + " ")   
            
            cln_Sentences = cln_sens[i]
            sens = raw_sens[i]
                
            for j in range(0, len(cln_Sentences)):   # Sentance Level
                searched_Text = text.findall(cln_Sentences[j], re.IGNORECASE)       
                                               
                if len(searched_Text) > 0:
                    doc_Found_Sens.append(sens[j])
                              
                if len(doc_Found_Sens) > 0:
                    doc_Presence = True
            
            word_Sens_Alldocs.append(doc_Found_Sens)                                   
            found_In_Doc.append(doc_Presence)
            
        all_Words_Sens.append(word_Sens_Alldocs)         
        word_Presence.append(found_In_Doc)

    return (word_Presence, all_Words_Sens)
###############################################################################

def export(n, k, w_list, wp, aws):
    """Dynamically names the titles of spreadsheets and columns, and exports"""
        
    # Helper function, generates ordinal numbers for naming the spreadsheets     
    def ordinal( m ):
    
        suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
    
        if m % 100 in (11,12,13):
            s = 'th'
        else:
            s = suffix[m % 10]
    
        return (str(m) + s)
        
        
    for i in range(0, n): 
          
        V1 = w_list[i]  
        V2 = wp[i] 
        V3 = aws[i] 
        
        df_2 = pd.DataFrame(V2, columns=['Present in Doc'])
        full_Table = df_2.set_value(0, 'Top ' + str(n) + ' Words: ' + 
                                                              ordinal(i+1), V1)
        full_Table = full_Table[['Top ' + str(n) + ' Words: ' + 
                                                ordinal(i+1),'Present in Doc']]
        
        for j in range(0, k):
    
            df_Var = pd.DataFrame(V3[j], columns=['Sentences in the ' + 
                                                   ordinal(j+1) + " Document"])
            full_Table = pd.concat([full_Table, df_Var], axis = 1)
    

        full_Table.to_excel('V2_test_Hashtags' + str(i)+ '.xlsx', 
                                            sheet_name='sheet1', index=False)
###############################################################################

def html_Highlight(n,  w_list, aws):
    """Searches sen's per common word, adds color highlight for html view"""

    high_Color = 'orange'
    
    for i in range(0, n):
        
        word = w_list[i]  
        sens_Vec = aws[i]
        highlt_Sens = []

        regex_Bold = re.compile(" " + word + " ")
        
        for docs in sens_Vec:        
            for sen in docs:
                                
                i = 0; output = "&lt;html&gt;"
                for m in regex_Bold.finditer(sen):
                    output += "".join([sen[i:m.start()],
                    "&lt;strong&gt;&lt;span style='color:%s'&gt;" % high_Color,
                       sen[m.start():m.end()], "&lt;/span&gt;&lt;/strong&gt;"])
                           
                    i = m.end()
                    
                highlt_Sens.append("".join([output, sen[m.end():],
                                                             "&lt;/html&gt;"]))
              
        df_HTML = pd.DataFrame(highlt_Sens, 
                                   columns=['Key Word Highlighted Sentences'])
    
        df_HTML.to_excel('Sentences where ' + word + " is present" + '.xlsx', 
                                              sheet_name='sheet1', index=False)
###############################################################################

def main():   
    """Runs all the classes by default. Takes user input"""
    
    docs_found = False
    while(docs_found == False):    
        
        dir_path = input("Enter the desired folder's path for analysis" 
                                                   + " (Without \"\" or '') :")                        
        n = int(input("Enter number of most common words you would like" + 
                                                  " to find (Enter an Int) :"))
#        dir_path = "C:\\Users\\Duwan_000\\test docs"
#        n = 320
        
        if n == 0:
            print("Error: Must enter int > 0...")
            docs_found = False
                 
        elif top_N(dir_path, n) == False:
            print("Error: Not enough text found in path...")
                 
        else:
            docs_found = True
       
    data = top_N(dir_path, n)    
    
    plot_Words(data[5], data[0], data[1])
    
    sen_data = sentences(data[5], data[2], data[3], data[4])
    
    export(n, data[2], data[6], sen_data[0], sen_data[1])
    
    html_Highlight(n, data[6], sen_data[1])
 ##############################################################################  

start_time = time.clock() #Begins runtime analysis     
main()
print("--- %s seconds ---" % (time.clock() - start_time))    