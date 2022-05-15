import pandas as pd
import os

def excel_creator(l):
    df1= pd.read_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/comments.xlsx',index_col=0)
    df2= pd.read_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/followers.xlsx',index_col=0)
    df3= pd.read_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/likes.xlsx',index_col=0)
    if l == ['comment']:
        df=df1.groupby(['Username']).agg(tuple).applymap(list).reset_index()
        df['Score']=len(df.Username)*[1]
        df=df.drop('Comment',axis=1)
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['mention'] or l == ['comment','mention']:
        df=df1.groupby(['Username']).agg(tuple).applymap(list).reset_index()
        c =[]
        i = 0
        while i < len(df.Comment):
            s=''
            for tag in df.Comment[i] :
                s += tag
            c.append((s.count('@')//5)+1)
            i += 1
        df['Score']=c
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['like']:
        df = df3
        df['Score']=len(df.Username)*[1]
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['follow']:
        df = df2
        df['Score']=len(df.Username)*[1]
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['comment', 'like'] or l == ['mention','like'] or l == ['comment','mention','like']:
        df=df1.groupby(['Username']).agg(tuple).applymap(list).reset_index()
        d={user:list(list(df.Username) + list(df3.Username)).count(user) for user in list(list(df.Username) + list(df3.Username))}
        users = d.keys()
        score = d.values()
        df = pd.DataFrame(zip(users,score),columns =['Username','Score'])
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['comment', 'follow'] or l == ['mention','follow'] or ['comment','mention','follow']:
        df=df1.groupby(['Username']).agg(tuple).applymap(list).reset_index()
        d={user:list(list(df.Username) + list(df2.Username)).count(user) for user in list(list(df.Username) + list(df2.Username))}
        users = d.keys()
        score = d.values()
        df = pd.DataFrame(zip(users,score),columns =['Username','Score'])
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df
    elif l == ['like', 'follow']:
        l = list(df2.Username) + list(df3.Username)
        d={user:list(l).count(user) for user in list(l)}
        users = d.keys()
        score = d.values()
        df = pd.DataFrame(zip(users,score),columns =['Username','Score'])
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')
        return df 
    elif l == ['comment', 'like', 'follow'] or l == ['mention','like','follow'] or l==['comment','mention','like','follow']:
        l = list(df1.Username)+list(df2.Username) + list(df3.Username)
        d={user:list(l).count(user) for user in list(l)}
        users = d.keys()
        score = d.values()
        df = pd.DataFrame(zip(users,score),columns =['Username','Score'])
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx')        
def winner_chooser():
    df= pd.read_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/final.xlsx',index_col=0)
    import random
    w=tuple(df.Score)
    Usernames = list(df.Username)
    winner=random.choices(Usernames, weights=w,cum_weights=None, k=1)[0]
    return (winner)

