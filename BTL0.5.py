###----Libraries: NLTK, TextBlob, TextStat, w3lib, 

import nltk
import urllib.request
import string
import urllib.error
from textblob import TextBlob
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import Counter
from urllib.request import Request, urlopen
from textstat import textstat
import w3lib.html
import w3lib.encoding

def remove_punctuation(value):
    result=""
    for c in value:
        if c not in string.punctuation:
            result += c
    return result

print(" Welcome to Between the Lines 0.5 Beta. \n What kind of text will you be analyzing today?")
######################################################################################################################
####-----------DEFINE-TAB-FUNCTION-------------------------------------------------------------------#############
#########################################################################################################################
def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))       
        except ValueError:
            print("Invalid input. Please enter a number: 1, 2, 3, or 4.")
            continue
        if userInput not in [1, 2, 3, 4]:
            print("Invalid integer. Please enter 1, 2, 3, or 4.")
            continue
##############################################################################################################
#######--------CHOICE-#1:-DOCUMENT-FILE----------------------------------------------------------##############
##############################################################################################################
        if userInput == 1:
            docchoice = input("Please enter the name of the Text File.\n")
            sourcedoc = open(docchoice, 'r')
            readsource = sourcedoc.read()
            lowfile = readsource.lower()
#            filesoup = BeautifulSoup(lowfile,'lxml')
#            filetext = filesoup.get_text(strip = True)
#            sent = TextBlob(filetext)
            sent = TextBlob(lowfile)
            slashsplice = sent.replace('/', ' ')
            dashsplice = (slashsplice.replace('-', ' '))
            dashsplice2 = (dashsplice.replace('–', ' '))
            sentblob = TextBlob(lowfile)
            filepunct = TextBlob(str(remove_punctuation(dashsplice2)))
            finaltext = str(remove_punctuation(dashsplice2))
            print("\n-----------------------------------------------")
            print("-----Sentiment Analysis Guide------------------")
            print("-----------------------------------------------")
            print("    Polarity(Emotion): \n    [ -1:Negative,   0:Neutral,   1:Positive ]")
            print("\n    Subjectivity(Fact VS Opinion): \n    [ 0:Objective    1:Subjective ]")
            print("------------------------------------------------")
            polar = sentblob.sentiment.polarity
            subject = sentblob.sentiment.subjectivity
            print("\n|------------------------------------|")
            print("|-----SENTIMENT ANALYSIS RESULTS-----|")
            print("|------------------------------------|")
            print("|    Polarity: ",polar, "                \n|    Subjectivity: ",subject,"            ")
            print("|------------------------------------|")
            tag_dict = {"J": 'a', 
                        "N": 'n', 
                        "V": 'v', 
                        "R": 'r'}    
            words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in filepunct.tags]    
            lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
            punctuate = str.maketrans('', '',string.punctuation)
            tokens = [w.translate(punctuate) for w in lemmatized_list]
#            splitpunct = filepunct.split()
            stoplist = stopwords.words('english')+['ie', 'may', 'us', 'shall', 'etc', 'thereof', '2', '1', '0', '–', '’','’','“','”']
#            tokens = [w for w in splitpunct]
            clean_tokens = tokens[:]
            for token in tokens:
                if token in stoplist:
                    clean_tokens.remove(token)
            count = Counter(clean_tokens)
            print("\n-------30 MOST COMMON WORDS-------: \n")
            for key, value in count.most_common(30):
                print("   "+ str(value)+ " - " +key)  
            print("\n-------FREQUENCY CHART-------:")
            freq = nltk.FreqDist(clean_tokens)
            freq.plot(15, cumulative=False) 
     ##---------------PHRASE (1,2,3,4 WORDS) COUNTER----------------------------------------
            bitokens = nltk.word_tokenize(finaltext)
            bgs = nltk.ngrams(bitokens, 2)
            fdist = nltk.FreqDist(bgs)
            count = fdist.most_common(10)
            tgs = nltk.ngrams(bitokens, 3)
            fdist2 = nltk.FreqDist(tgs)
            count2 = fdist2.most_common(10)
            qgs = nltk.ngrams(bitokens, 4)
            fdist3 = nltk.FreqDist(qgs)
            count3 = fdist3.most_common(10)
            print("\n--------COMMON PHRASES (2 WORDS)--------:\n")
            for (key, key2), value in count:
                print("   ",key,"",key2,"","-",value)
            print("\n--------COMMON PHRASES (3 WORDS)--------:\n")
            for (key, key2, key3), value in count2:
                print("   ",key,"",key2,"",key3,"-",value)
            print("\n--------COMMON PHRASES (4 WORDS)--------:\n")
            for (key, key2, key3, key4), value in count3:
                print("   ",key,"",key2,"",key3,"",key4,"-",value)
####---------------------READABILITY INDEX--------------------###########
            flesh = int(textstat.flesch_reading_ease(readsource))
            print("--------FLESCH-KINCLAID TEST--------\n", "\n    Readability Score: ",flesh)
            if flesh in range(0,30):
                print("    Very difficult to read. Best understood by university graduates.")
            if flesh in range(31,50):
                print("    Difficult to read.")
            if flesh in range(51, 60):
                print("    Fairly difficult to read.")
            if flesh in range(61, 70):
                print("    Plain English. Easily understood by 13- to 15-year-old students.")
            if flesh in range(71,80):
                print("    Fairly easy to read.")    
            if flesh in range(81,90):
                print("    Fairly easy to read.")
            if flesh in range(90,100):
                print("    Very easy to read. Easily understood by an average 11-year-old student.")
            print("-----------------------------------\n")

     ##################---END. LOOP---##########################################################################################################
            again = input("\nThank you for using BTL 0.6. Run Again? [Y / N]\n")
            acceptable = ["Y", "y", "N", "n"]
            if again in ["Y", "y"]:
                print("What kind of document?")
                return inputNumber(message)
            if again in ["N", "n"]:
                quit()
            while again not in acceptable:
                print("\nSorry, didn't catch that. Please select an option below:")
                return inputNumber(message)
            break
        
        
##############################################################################################################
####----------CHOICE-#2:-URL/LINK-------------------------------------------------------------------------------
##############################################################################################################
        if userInput == 2:
            webchoice = input("Please enter the URL of the website.\n")
            webdoc =  urllib.request.urlopen(webchoice)
            readweb = webdoc.read()
            websoup = w3lib.html.remove_tags(readweb)
#            websoup = BeautifulSoup(readweb,'html5lib')
          #  websoup2 = websoup.text
            print(websoup)
            lowweb = websoup.lower()
            websent = TextBlob(lowweb)
            slashsplice = websent.replace('/', ' ')
            dashsplice = (slashsplice.replace('-', ' '))
            dashsplice2 = (dashsplice.replace('–', ' '))
            dashsplice3 = (dashsplice2.replace(' – ',' '))
            pagesplice = dashsplice3.replace(' p. ', ' ')
            pagesplice2 = pagesplice.replace(' pp.', ' ')
            webpunct = TextBlob(str(remove_punctuation(pagesplice2)))
            finalweb = str(remove_punctuation(pagesplice2))
            print("\n-----------------------------------------------")
            print("-----Sentiment Analysis Guide------------------")
            print("-----------------------------------------------")
            print("    Polarity(Emotion): \n    [ -1:Negative,   0:Neutral,   1:Positive ]")
            print("\n    Subjectivity(Fact VS Opinion): \n    [ 0:Objective    1:Subjective ]")
            print("------------------------------------------------")
            polar = websent.sentiment.polarity
            subject = websent.sentiment.subjectivity
            print("\n|------------------------------------|")
            print("|-----SENTIMENT ANALYSIS RESULTS-----|")
            print("|------------------------------------|")
            print("|    Polarity: ",polar, "                \n|    Subjectivity: ",subject,"            ")
            print("|------------------------------------|")
            tag_dict = {"J": 'a', 
                        "N": 'n', 
                        "V": 'v', 
                        "R": 'r'}    
            words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in webpunct.tags]    
            lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
            punctuate = str.maketrans('', '',string.punctuation)
            tokens = [w.translate(punctuate) for w in lemmatized_list]
            stoplist = stopwords.words('english')+['ie', 'may', 'us', 'shall', 'etc', 'thereof', " ", 'mwparseroutput', 'wwww3org', 'xmlnshttp', 'also', '1', '0', 'svg', '2', 'jw','’','“','”', 'u']  
            clean_tokens = tokens[:]
            for token in tokens:
                if token in stoplist:
                    clean_tokens.remove(token)
            count = Counter(clean_tokens) 
            print("\n---------MOST COMMON WORDS---------: \n")
            for key, value in count.most_common(30):
                print("   "+key+ " - " + str(value)) 
            print("\n---------FREQUENCY CHART---------:")
            freq = nltk.FreqDist(clean_tokens)
            freq.plot(10, cumulative=False)    
     #################################################################################################
     ##---------------PHRASE (1,2,3,4) COUNTER----------------------------------------
     ###################################################################################
            bitokens = nltk.word_tokenize(finalweb)
            bgs = nltk.ngrams(bitokens, 2)
            fdist = nltk.FreqDist(bgs)
            count = fdist.most_common(20)
            tgs = nltk.ngrams(bitokens, 3)
            fdist2 = nltk.FreqDist(tgs)
            count2 = fdist2.most_common(20)
            qgs = nltk.ngrams(bitokens, 4)
            fdist3 = nltk.FreqDist(qgs)
            count3 = fdist3.most_common(20)
            print("\n--------COMMON PHRASES (2 WORDS)--------:\n")
            for (key, key2), value in count:
                print("   ",key,"",key2,"","-",value)
            print("\n--------COMMON PHRASES (3 WORDS)--------:\n")
            for (key, key2, key3), value in count2:
                print("   ",key,"",key2,"",key3,"-",value)
            print("\n--------COMMON PHRASES (4 WORDS)--------:\n")
            for (key, key2, key3, key4), value in count3:
                print("   ",key,"",key2,"",key3,"",key4,"-",value)
     #################################################################################################
     ##---------------READABILITY INDEX----------------------------------------
     ###################################################################################
     ##########---------------END LOOP---------------------##############################
            again = input("\nThank you for using BTL 0.6. Run Again? [Y / N]")
            acceptable = ["Y", "y", "N", "n"]
            if again in ["Y", "y"]:
                print("What kind of document?")
                return inputNumber(message)
            if again in ["N", "n"]:
                print("Bye!")
                quit()
            while again not in acceptable:
                print("\nSorry, didn't catch that. Please select an option below:")
                return inputNumber(message)
            break


        
########################################################################################################################
############--------CHOICE-#3:-MANUAL-INPUT----------########################################
############################################################################################################


        if userInput == 3:
            manchoice = input("Please enter your text here:\n")
            lowman = manchoice.lower()
            mansoup = BeautifulSoup(lowman,'html5lib')
            mantext = mansoup.get_text(strip = True)
            mansent = TextBlob(mantext)
            sent = TextBlob(manchoice)
            manpunct = TextBlob(str(remove_punctuation(mansent)))
            finalman = str(remove_punctuation(mansent))
            splitpunct = manpunct.split()
            stoplist = stopwords.words('english')+['ie', 'may', 'us', 'shall', 'etc', 'thereof', '0', '–','’','“','”','’']
            print("\n-----------------------------------------------")
            print("-----Sentiment Analysis Guide------------------")
            print("-----------------------------------------------")
            print("    Polarity(Emotion): \n    [ -1:Negative,   0:Neutral,   1:Positive ]")
            print("\n    Subjectivity(Fact VS Opinion): \n    [ 0:Objective    1:Subjective ]")
            print("------------------------------------------------")
            polar = sent.sentiment.polarity
            subject = sent.sentiment.subjectivity
            print("\n|------------------------------------|")
            print("|-----SENTIMENT ANALYSIS RESULTS-----|")
            print("|------------------------------------|")
            print("|    Polarity: ",polar, "                \n|    Subjectivity: ",subject,"            ")
            print("|------------------------------------|")
            tag_dict = {"J": 'a', 
                        "N": 'n', 
                        "V": 'v', 
                        "R": 'r'}    
            words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in manpunct.tags]    
            lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
            punctuate = str.maketrans('', '',string.punctuation)
#            tokens = [w.translate(punctuate) for w in lemmatized_list]
            tokens = [w for w in splitpunct]
            stoplist = stopwords.words('english')+['ie', 'may', 'us', 'shall', 'etc', 'thereof', '—']
            clean_tokens = tokens[:]
            for token in tokens:
                if token in stoplist:
                    clean_tokens.remove(token)                
            count = Counter(clean_tokens)    
            print("\n------35 MOST COMMON WORDS------: \n")
            for key, value in count.most_common(35):
                print("   "+key+ " - " + str(value)) 
            print("\n------FREQUENCY CHART------:")
            freq = nltk.FreqDist(clean_tokens)
            freq.plot(10, cumulative=False)  
     #################################################################################################
     ##---------------PHRASE (1,2,3,4 WORDS) COUNTER----------------------------------------
     ##################################################################################
            bitokens = nltk.word_tokenize(finalman)
            bgs = nltk.ngrams(bitokens, 2)
            fdist = nltk.FreqDist(bgs)
            count = fdist.most_common(10)
            tgs = nltk.ngrams(bitokens, 3)
            fdist2 = nltk.FreqDist(tgs)
            count2 = fdist2.most_common(10)
            qgs = nltk.ngrams(bitokens, 4)
            fdist3 = nltk.FreqDist(qgs)
            count3 = fdist3.most_common(10)
            print("\n--------COMMON PHRASES (2 WORDS)--------:\n")
            for (key, key2), value in count:
                print("   ",key,"",key2,"","-",value)
            print("\n--------COMMON PHRASES (3 WORDS)--------:\n")
            for (key, key2, key3), value in count2:
                print("   ",key,"",key2,"",key3,"-",value)
            print("\n--------COMMON PHRASES (4 WORDS)--------:\n")
            for (key, key2, key3, key4), value in count3:
                print("   ",key,"",key2,"",key3,"",key4,"-",value,)
      ######---------------READABILITY INDEX#----------------####   
            flesh = int(textstat.flesch_reading_ease(manchoice))
            print("\n----------FLESCH-KINCLAID TEST----------:\n", "\n    Readability Score: ",flesh, "\n")
            if flesh in range(0,31):
                print("    --Very difficult to read. Best understood by university graduates.--")
            if flesh in range(31,51):
                print("    --Difficult to read.--")
            if flesh in range(51, 61):
                print("    --Fairly difficult to read.--")
            if flesh in range(61, 71):
                print("    --Plain English. Easily understood by 13 to 15-year-old students.--")
            if flesh in range(71,81):
                print("    --Fairly easy to read.--")    
            if flesh in range(81,91):
                print("    --Fairly easy to read.--")
            if flesh in range(91,100):
                print("    --Very easy to read. Easily understood by an average 11-year-old student.--")
            print("\n------------------------------------------\n")
     
            again = input("\nThank you for using BTL 0.3. Run Again? [Y / N]")
            acceptable = ["Y", "y", "N", "n"]
            if again in ["Y", "y"]:
                print("What kind of document?")
                return inputNumber(message)
            if again in ["N", "n"]:
                print("Bye!")
                quit()
            while again not in acceptable:
                print("\nSorry, didn't catch that. Please select an option below:")
                return inputNumber(message)
            break
###################################################################################################################
##########---------CHOICE 4: QUIT PROGRAM-------------------------------------------------------------------------------
######################################################################################################################
        if userInput == 4:
            print("Thank you for using BTL 0.5. Bye!")
            quit()
            break
#---------------------------------------------------------------------------------------------------------------        
########################################################################################################################            
#------------EXECUTE PROGRAM------------------------------------------------------------------------------            
########################################################################################################################
#---------------------------------------------------------------------------------------------------------------
            
inputNumber(" [1] = Text File. \n [2] = URL. \n [3] = Enter Manually. \n [4] = Quit\n \n ")

################################################################################################################################
