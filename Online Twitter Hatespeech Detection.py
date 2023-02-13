#Access Token:1578809428488622080-O2G7wVsE23HAD5trS85WSuDeHQjNyg
#Access Token Secret:QEKAvkwPzaeVwVlV6PIverEjTtmDUd8wiDceDtXwCYpb8

import tweepy
import pandas as pd
import string
from textblob import TextBlob
import re
import nltk
from deep_translator import GoogleTranslator
translator = GoogleTranslator()


Bearer_token="AAAAAAAAAAAAAAAAAAAAAL%2BgkQEAAAAALCzScbG8Q%2BAKftddVXXggfHHeps%3DXUcI0KLnh39LKOoU1nw0xeQuQaQvxIYkuTsazuFfOiMlZ4fz8L"          
Consumer_key="X1pMCOqpAn3jb7rUeRAdNIJIx"
Consumer_secret="NlKH5g4uMwvJjuyGuWw7us09OfnxtPdxwtme9p4nqpgonFWBgL"
Access_key="1578809428488622080-xrGc7hVQTITEZFUr5jxzB5AyNkofJw"
Access_secret="BFTmKobf2FW21fjsW49z7fpXs7tH3QV8fJujqqm6VHHer"


def getClient():
        client=tweepy.Client(bearer_token=Bearer_token,
                             consumer_key=Consumer_key,
                             consumer_secret=Consumer_secret,
                             access_token=Access_key,
                             access_token_secret=Access_secret,
                              return_type=dict)
        print("Enter Twitter HashTag to search for")
        words = input()
        Tweets=client.search_recent_tweets(query=words,max_results=100)
        return Tweets
User=getClient()
#print(User)

#Importing to list dict.values
list1=[]
for i in User['data']:
    list1.append(i['text'])
#print(list1)



#Translating the data
languages_list=[]
for i in list1:
    translated=GoogleTranslator(source='auto',target='english').translate(i)
    #print(translated)
    languages_list.append(translated)
#print(languages_list)


#Data Cleaningdef clean_text(df):
def clean_text(df):
    all_reviews=[]
    for text in df:
        text.lower()
        pattern=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        text=pattern.sub('',text)
        
        emoji=re.compile("["
                           u"\U0001F600-\U0001FFFF"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        text=emoji.sub('',text)
        all_reviews.append(text)
    return all_reviews
all_reviews=clean_text(languages_list)
#print(all_reviews)

df=pd.DataFrame(all_reviews,columns =['Review'])
#print(df)

polarity_score=[]

for i in range(0,df.shape[0]):
        score=TextBlob(df.iloc[i][0])
        score1=score.sentiment[0]
        polarity_score.append(score1)

df=pd.concat([df,pd.Series(polarity_score)],axis=1)
df.rename(columns={df.columns[1] :'Sentiments'},inplace=True)
#print(df)


ptweets=[]
ntweets=[]

for i in range(0,len(df['Sentiments'])):
        if df['Sentiments'][i]>0:
                        ptweets.append(df['Review'][i])
                        
        elif df['Sentiments'][i]<0:
                        ntweets.append(df['Review'][i])
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(df)))
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(df)))
print("Neutral tweets percentage: {} % \
        ".format(100*(len(df) -(len( ntweets )+len( ptweets)))/len(df)))
print('positive tweets:______________________________________')
for i in ptweets:
        print(i,'/n')
print('negative tweets:______________________________________')
for i in ntweets:
        print(i,'/n')        








