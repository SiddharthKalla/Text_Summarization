# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 01:36:52 2020

@author: leno
"""

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text = ''' Widely hailed as a masterpiece of rhetoric, King's speech invokes pivotal documents 
           in American history, including the Declaration of Independence, the Emancipation Proclamation, 
           and the United States Constitution. Early in his speech, King alludes to Abraham Lincoln's 
           Gettysburg Address by saying "Five score years ago ..." In reference to the abolition of 
           slavery articulated in the Emancipation Proclamation, King says: "It came as a joyous 
           daybreak to end the long night of their captivity." Anaphora (i.e., the repetition of a 
           phrase at the beginning of sentences) is employed throughout the speech. Early in his speech, 
           King urges his audience to seize the moment; "Now is the time" is repeated three times in the sixth 
           paragraph. The most widely cited example of anaphora is found in the often quoted phrase 
           "I have a dream", which is repeated eight times as King paints a picture of an integrated and 
           unified America for his audience. Other occasions include "One hundred years later", "We can 
           never be satisfied", "With this faith", "Let freedom ring", and "free at last". King was the 
           sixteenth out of eighteen people to speak that day, according to the official program.'''

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_sm')

doc = nlp(text)

tokens = [token.text for token in doc ]

punctuation = punctuation + '\n' + ' ' + '  ' + '...' + '\n           '

word_frequency = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1
                
max_frequency = max(word_frequency.values())

for word in word_frequency.keys():
    word_frequency[word] = word_frequency[word]/max_frequency
                
sentence_tokens = [sent for sent in doc.sents]

sentence_score = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequency.keys():
            if sent not in sentence_score.keys():
                sentence_score[sent] = word_frequency[word.text.lower()]
            else:
                sentence_score[sent] += word_frequency[word.text.lower()]
                
from heapq import nlargest 

select_length = int(len(sentence_tokens)*0.3)

summary = nlargest(select_length, sentence_score, key = sentence_score.get)                
                
final_summary = [word.text for word in summary]

summary = ' '.join(final_summary)

len(text)
len(summary)