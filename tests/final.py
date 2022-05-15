import pandas as pd
from instaloader.instaloader import Instaloader
from instaloader.structures import Post ,Profile
import os
from pathlib import Path
df= pd.read_excel('comments.xlsx',index_col=0)


df2=df.groupby(['Username']).agg(tuple).applymap(list).reset_index()


d={user:list(df.Username).count(user) for user in list(df.Username)}
Comment_num = d.values()
df2['Comment_number']=Comment_num

comments=list(df2.Comment)
print(comments)
c=0
a=[]
for tag in comments :
    a.append( tag.count('@'))
ts=[i//5 for i in a]
print(a)
print(ts)
df2['Tag Score']= ts


df1= pd.read_excel('followers.xlsx',index_col=0)
follower = list(df1.Username)
user=list(df2.Username)
s=[]
for i in user :
    if i in follower :
        s.append(1)
    else:
        s.append(0)
df2['Follow'] = s


df3= pd.read_excel('likes.xlsx',index_col=0)
likes = list(df3.Username)
user=list(df2.Username)
s=[]
for i in user :
    if i in likes :
        s.append(1)
    else:
        s.append(0)
df2['Like'] = s





df2['Score']=len(df2)*[0]
s = list(df2.sum(axis=1))
df2['Score']=s
df2.to_excel('final.xlsx')
print(df2)


import random
w=tuple(df2.Score)
Usernames = list(df2.Username)
winner=random.choices(Usernames, weights=w,cum_weights=None, k=1)[0]
print(winner)
