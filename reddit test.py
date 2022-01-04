"""
import requests
import pandas as pd
from datetime import datetime

CLIENT_ID = 'Redacted'
SECRET_TOKEN = 'Redacted'

# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            #'upvote_ratio': post['data']['upvote_ratio'],
            #'ups': post['data']['ups'],
            #'downs': post['data']['downs'],
            #'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            #'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df

# authenticate API
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
data = {
    'grant_type': 'password',
    'username': 'Redacted',
    'password': 'Redacted'
}
headers = {'User-Agent': 'FilterFeedBot/0.01'}

# send authentication request for OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)
# extract token from response and format correctly
TOKEN = f"bearer {res.json()['access_token']}"
# update API headers with authorization (bearer token)
headers['Authorization'] = TOKEN

# initialize dataframe and parameters for pulling data in loop
data = pd.DataFrame()
params = {'limit': 100}

# loop through 10 times (returning 1K posts)
for i in range(1):
    # make request
    res = requests.get("https://oauth.reddit.com/r/legomarket/new",
                       headers=headers,
                       params=params)

    # get dataframe from response
    new_df = df_from_response(res)
    # take the final row (oldest entry)
    row = new_df.iloc[len(new_df)-1]
    # create fullname
    fullname = row['kind'] + '_' + row['id']
    # add/update fullname in params
    params['after'] = fullname
    
    # append new_df to data
    data = data.append(new_df, ignore_index=True)

for post in data['title']:
    if 'UK' in post:
        if '[US' not in post:
            print(post)

"""
import praw
from datetime import datetime

CI = '3tOYxW_VpzQEMkCay6tKNQ'
ST = 'lu-8ZvMrjioER6Fl_5Em8lS8wOzRvg'
VERSION = 'FilterFeedBot/0.01'

reddit = praw.Reddit(client_id = CI, client_secret = ST, user_agent = VERSION)

lm = reddit.subreddit("Legomarket")

def getNewPost(counter):
    newest = ""
    for post in lm.new(limit=10, params={'before': counter}):
        print(f'{post.title}\n{post.shortlink} - {post.fullname}, {datetime.fromtimestamp(post.created_utc)}')
        if newest == "":
            print("newest: ", post.fullname)
            newest = post.fullname
    return newest if newest != "" else counter

a = 't3_rkfnxt'

for x in range(10):
    a = getNewPost(a)

