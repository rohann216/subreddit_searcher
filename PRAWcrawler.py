import praw
import pandas as pd
import os

MINIMUM_SCORE = 0 # minimum score of posts to show

reddit = praw.Reddit(client_id="CLIENT_ID",         # your client id
                     client_secret="CLIENT_SECRET",      # your client secret
                     username='USERNAME', # reddit username
                     password='PASSWORD', # reddit password
                     user_agent="USER_AGENT")        # your user agent

subreddits = []

with open('subreddits.csv', 'r') as file:
    for line in file:
        subreddit = line.strip()  # Remove leading/trailing whitespaces
        subreddits.append(subreddit)

# Set keywords to search for
keywords = []

# Iterate through each subreddit
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name.strip())
    
    # Create an empty DataFrame to store the post information
    columns = ['Subreddit', 'Keyword', 'Title', 'Date', 'Score', 'Comments', 'URL']
    df = pd.DataFrame(columns=columns)

    # Search for posts that relate to keyword
    for keyword in keywords:
        posts = subreddit.search(keyword, sort='new', time_filter='all', syntax='lucene', limit = None)

        # Append to data frame
        for post in posts:
                if post.score >= MINIMUM_SCORE:
                    post_info = {
                        'Subreddit': subreddit_name,
                        'Keyword': keyword,
                        'Title': post.title,
                        'Date': pd.to_datetime(post.created_utc, unit='s').date(),
                        'Score': post.score,
                        'Comments': post.num_comments,
                        'URL': post.url
                    }
                    df = pd.concat([df, pd.DataFrame(post_info, index=[0])], ignore_index=True)
    print(df)
    print("\n")

    file_name = os.path.join("subreddit_info", subreddit_name + '.csv')
    df.to_csv(file_name, index=True)