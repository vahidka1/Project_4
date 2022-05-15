from instaloader.instaloader import Instaloader
from instaloader.structures import Post ,Profile
import os
import json
import pandas as pd

if not os.path.exists(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/'):
    os.mkdir(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/')

if not os.path.exists(r'E:/barname_nevisi/python/pybootcamp/mian_term/comments'):
    os.mkdir(r'E:/barname_nevisi/python/pybootcamp/mian_term/comments')


def post(url):
    return url +' '+'embed&amp;utm_campaign=loading'

def scrapecomment(url):
    
    try:
        insta= Instaloader(sleep=True, quiet=False, user_agent=None, dirname_pattern=None, filename_pattern=None, download_pictures=False, download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=True, save_metadata=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None, max_connection_attempts=10, request_timeout=300.0, rate_controller=None, resume_prefix='iterator', check_resume_bbd=True, slide=None, fatal_status_codes=None, iphone_support=True)
        insta.login(user='pyinston',passwd='v13781378')
        dir = 'E:/barname_nevisi/python/pybootcamp/mian_term/comments'
        files = os.listdir(dir)
        for file in files:
         os.remove(os.path.join(dir, file))
        shortpost=url.split('/')
        post=Post.from_shortcode(insta.context,shortpost[4])
        insta.download_post(post,target='comments')
        return(post.owner_username)
        

    except Exception as ex :
        return ex

    
def scrapefollowers(url):
    shortpost=url.split('/')
    try:
        insta= Instaloader(sleep=True, quiet=False, user_agent=None, dirname_pattern=None, filename_pattern=None, download_pictures=False, download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=True, save_metadata=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None, max_connection_attempts=10, request_timeout=300.0, rate_controller=None, resume_prefix='iterator', check_resume_bbd=True, slide=None, fatal_status_codes=None, iphone_support=True)
        insta.login(user='pyinston',passwd='v13781378')
        post=Post.from_shortcode(insta.context,shortpost[4])
        username=post.owner_username
        profile = Profile.from_username(insta.context, username)
        followers=[]
        for follower in profile.get_followers():
            followers.append(follower.username)
        df = pd.DataFrame(followers,columns =['Username'])
        print(df)
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/followers.xlsx')
    except Exception as ex :
        return ex

def scrapelikes(url):
    shortpost=url.split('/')
    try:
        insta= Instaloader(sleep=True, quiet=False, user_agent=None, dirname_pattern=None, filename_pattern=None, download_pictures=False, download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=True, save_metadata=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None, max_connection_attempts=10, request_timeout=300.0, rate_controller=None, resume_prefix='iterator', check_resume_bbd=True, slide=None, fatal_status_codes=None, iphone_support=True)
        insta.login(user='pyinston',passwd='v13781378')
        post=Post.from_shortcode(insta.context,shortpost[4])
        likes=[]
        for like in post.get_likes():
            likes.append(like.username)
        df = pd.DataFrame(likes,columns =['Username'])
        print(df)
        df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/likes.xlsx')
    except Exception as ex :
        return ex
def jsontoexel():
    dir = 'E:/barname_nevisi/python/pybootcamp/mian_term/comments'
    files = os.listdir(dir)
    for file in files:
        if file[-4:] =='json':
            json_file = open(dir+'/'+file)
            data = json_file.read()
            comments = json.loads(data)
            #print(comments['username'],comments['owner']['text'])
            print(len(comments))
            user_names = []
            user_comments = []
            i=0
            while i < len(comments):
                user = (comments[i]['owner']['username'])
                comment =(comments[i]['text'])
                user_names.append(user)
                user_comments.append(comment)
                i += 1
            df = pd.DataFrame(list(zip(user_names, user_comments)),columns =['Username', 'Comment'])
            print(df)
            
            df.to_excel(r'E:/barname_nevisi/python/pybootcamp/mian_term/static/files/comments.xlsx')

