# TF-IDF
Implements a Text-Frequency Inverse Document Frequency program for analysis of documents 

# Dependencies - python modules

matplotlib.pyplot
pandas
numpy
re
os 
collections: Counter
wordcloud : WordCloud


# Known Limitations
1. Does not implement an exhaustive grammatical analysis of the text. Errors or 
   pathological text could dramatically affect the resulting exported sentences.
2. Not tested on foreign/rare document encodings
3. Bar graph loses visual usefulness after n > 20 common words


# API

I:  top_N(dir_path, n)
    
    1. Finds top n occurrences of words in any documents, and cleans the text 
        for use by other methods

    Input:
    dir_path - path to a directory
    n - number of most common words desired to find
    
    Returns:
    common_Dict - Dictionary of n most common words and associated frequencies
    all_Words - List of all unique words
    docs_len - Length of documents read from directory 
    all_Cln_Sens - List of all sentences without punctuation
    all_Raw_Sens - List of all sentences with punctuation
    word - tuple of n common words
    word_List - List form of 'word' variable
    
    a)    
      Additionally, this method:
          
        i) removes the periods from common abbreviations 
           such as U.S., Mr., etc. before prior to the data being split into
           sentences.  
           
         ii) Removes question marks, exclamation marks, and periods that are
             likely grammatical mistakes. For example, in document 4, there 
             are a number of sentences like the following:
                 
          "Dreams of democracy and hopes for a perfect government are now 
            just that ? dreams and hopes."
            
            Clearly the question mark here is a mistake, and should not be 
            considered the end of a sentence. 
    

II:    plot_Words(com_word, common_Dict, all_words)
        
        2: Plotting and Data Visualization           
        
        Input: 
        com_word - 'word' variable from top_N() 
        common_Dict - from top_N()
        all_words - from top_N()
        
        Returns: 
        NA - Generates plots 
                
    a) The first graph is a bar graph that lists the top n most common words
        in order of decreasing frequency. 

    b) The second plot is a "WordCloud" that shows all of the common words
         arranged around each other. The most common word is the biggest, 
         followed by the second one, etc. 
         
        My implementation of wordcloud is adapted from: 
        https://github.com/amueller/word_cloud


III:   sentences(com_word, docs_len, cln_sens, raw_sens)
        
    3: Determining presence of word in docs, and finding 
       sentences of occurrence.
        
        Input: 
        com_word - 'word' variable from top_N() 
        docs_len - docs_len from top_N()
        cln_sens - all_Cln_Sens from top_N()
        raw_sens - all_Raw_Sens from top_N()    
        
        Returns: 
        word_Presence - Boolean list of lists, True if word found in i'th doc
        all_Words_Sens - list of lists: all sentences with i'th word in docs
                    
       a) This method searches the sentences of the docs for each of the 
            common words. All sentences with that word are added to a list of 
            lists. 

            If this list has even one sentence found, the doc_Presence list is
            appended with a "True" value.  
            
            These lists are used to fill up the spreadsheets generated with 
            the export method. 


IV:    export(n, k, w_list, wp, aws)
        
        4: Export of Results to excel/csv spreadsheets    

        Input: 
        n - number of common words searched
        k - docs_len from top_N()
        w_list - list of the common words from top_N()
        wp - word_Presence from sentence()
        asw - all_Words_Sens from sentence()    
    
        Returns: 
        NA - Exports panda dataframes to excel
        
        a) The export to excel produces a dynamical number of spreadsheets
            and number of columns that is dependent on the number of k
            documents analyzed.  

        b) I chose to implement an excel export since it presents the results 
            in an organized way that is also quickly transferable to further 
            analysis or for analysis that does not require a coding background. 
            
            
V:     html_Highlight(n,  w_list, aws)

        5. Highlights the i'th word in sentences for easier visual analysis
        
        Input: 
        n - number of common words searched
        w_list - list of the common words from top_N()
        asw - all_Words_Sens from sentence() 
        
        Returns:
        NA - Exports panda dataframes to excel.
        
        Searches sen's per common word, adds color highlight for the ith top 
        words. The output is HTML for viewing the sentences in a browser. 

        a) Additionally, I have adapted this function from :
            
   https://www.saltycrane.com/blog/2007/10/using-pythons-finditer-to-highlight/
   
       to create the html friendly highlighting output.
