import pandas as pd
import os

POSTS_COUNT = 5 # number of posts to show

def list_top_posts(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('./subreddit_info/' + csv_file)
    
    # Group the DataFrame by the "Keyword" column
    grouped_df = df.groupby('Keyword')
    
    # Process each group
    for keyword, group in grouped_df:
        # Sort the group by the "Score" column in descending order
        sorted_group = group.sort_values(by='Score', ascending=False)
        
        # Get the top POSTS_COUNT posts based on the sorted group
        top_posts = sorted_group.head(POSTS_COUNT)
        
        # Display the top POSTS_COUNT posts for the current keyword
        print(f"Top" + POSTS_COUNT + "posts for '{keyword}' in {csv_file}:")
        print(top_posts)
        print('\n')

        # Save the top POSTS_COUNT posts for the current keyword to a separate file
        keyword_file = keyword.replace(' ', '_')
        keyword_path = os.path.join('top_posts', keyword_file + '_' + csv_file)
        top_posts.to_csv(keyword_path, index=False)

# List of CSV files
folder_path = './subreddit_info'

csv_files = []

# Iterate over files in the folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        csv_files.append(file)

# Print the list of CSV file names
print(csv_files)


# Process each CSV file
for file in csv_files:
    list_top_posts(file)