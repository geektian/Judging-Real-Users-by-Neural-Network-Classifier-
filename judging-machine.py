#!/usr/bin/env python
# coding: utf-8

# In[15]:


# -*- coding: UTF-8 -*-
from __future__ import print_function
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import os
import csv
import winreg
#import sys
#import ctypes
# use natural language toolkit

# word stemmer
stemmer = LancasterStemmer()


# In[4]:


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')#利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0] #返回的是Unicode类型数据
if __name__=='__main__':
    Desktop_path=str(get_desktop())#Unicode转化为str
    #os.path.join(Desktop_path,output.csv)
    #sys_temp =str( os.getenv("TEMP"))
    #print(sys_temp)


# In[5]:


def lwalk(top, topdown=True, followlinks=False, max_level=None):
    if max_level is None:
        new_max_level = None
    else:
        if max_level==0:
            return
        else:
            new_max_level = max_level-1
    top = os.fspath(top)
    dirs, nondirs, walk_dirs = [], [], []
    with os.scandir(top) as it:
        for entry in it:
            if entry.is_dir():
                dirs.append(entry.name)
            else:
                nondirs.append(entry.name)
            if not topdown and entry.is_dir():
                if followlinks or not entry.is_symlink():
                    walk_dirs.append(entry.path)
        if topdown:
            yield top, dirs, nondirs
            for dirname in dirs:
                new_path = os.path.join(top, dirname)
                if followlinks or not os.path.islink(new_path):
                    yield from lwalk(new_path, topdown, followlinks, new_max_level)
        else:
            for new_path in walk_dirs:
                yield from lwalk(new_path, topdown, followlinks, new_max_level)
            yield top, dirs, nondirs


# In[6]:



    #print(dirs)
    #with open(os.path.join(Desktop_path,"data.csv"), "a") as f:
        #a=[dirs]
       # writer = csv.writer(f)
       # writer.writerows(a)


# In[7]:


#training_data
training_data = []
training_data.append({"class":"true", "sentence":"example"})

training_data.append({"class":"flase", "sentence":"example"})

#print ("%s sentences of training data" % len(training_data))


# In[8]:


# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
#print ("Class words: %s" % class_words)


# In[9]:


# we can now calculate a score for a new sentence
sentence = "good day for us to have lunch?"

# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1
            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score


# In[10]:


# now we can find the class with the highest score
#for c in class_words.keys():
 #   print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))


# In[11]:


# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score


# In[12]:


# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class#, high_score


# In[16]:


for root, dirs, files in lwalk("C:\Program Files (x86)" ,max_level=1):
    collected_dirs = str(dirs)
#classify("example")
#for root, dirs, files in lwalk(Desktop_path,max_level=3):
    #collected_dirs = str(dirs)
#classify("example")
#for root, dirs, files in lwalk(sys_temp ,max_level=1):
    #collected_dirs = str(files)
#classify("example")


# In[17]:


br= classify(collected_dirs)
tr='true'
if br == tr:
    file_object = open(os.path.join(Desktop_path,"运行成功了！.txt"), 'w')
    file_object.write("运行成功了！")
    file_object.close( )
else:
    file_object = open(os.path.join(Desktop_path,"没有运行！.txt"), 'w')
    file_object.write("没有运行！")
    file_object.close( )
print(br)

