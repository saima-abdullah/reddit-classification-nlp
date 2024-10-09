import pandas as pd
import requests
import time
import getpass
import os

client_id = getpass.getpass()#alphanumeric string provided under "personal use script"
client_secret = getpass.getpass() #alphanumeric string provided as "secret"
user_agent = getpass.getpass() #the name of your application
username =  getpass.getpass()#your reddit username
password =  getpass.getpass()#your reddit password'''


# Authenticate with Reddit API
def get_reddit_access_token(client_id, client_secret, username, password, user_agent):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type': 'password', 'username': username, 'password': password}
    headers = {'User-Agent': user_agent}
    
    #  access token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    headers['Authorization'] = f'bearer {token}'
    return headers

#fetch posts from a subreddit 
def get_subreddit_posts(headers, subreddit, sort='hot', time_filter='all', limit=100, after=None):
    url = f'https://oauth.reddit.com/r/{subreddit}/{sort}?limit={limit}&t={time_filter}'
    if after:
        url += f"&after={after}"  # Add pagination token to the request if available
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")  # Check the response status code
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
    return None

#  extract relevant post data (title, content, post id, and time)
def extract_post_data(subreddit_posts):
    post_data = []
    if 'data' in subreddit_posts:
        for post in subreddit_posts['data']['children']:
            post_info = {
                'post_id': post['data']['id'],
                'title': post['data']['title'],
                'content': post['data']['selftext'],
                'created_utc': post['data']['created_utc'],
                'subreddit': post['data']['subreddit']
            }
            post_data.append(post_info)
    return post_data

# get unique posts 
def fetch_reddit_data(client_id, client_secret, username, password, user_agent, subreddit, sorting_methods, time_filters, total_posts_per_subreddit):
    headers = get_reddit_access_token(client_id, client_secret, username, password, user_agent)
    print(headers)  # Print the headers to verify the access token

    all_posts = []
    post_ids = set()  # set to keep track of unique post IDs
    after = None  # Initialize 'after' for pagination

    for sorting_method in sorting_methods:
        for time_filter in time_filters:
            while len(all_posts) < total_posts_per_subreddit:
                try:
                    response_json = get_subreddit_posts(headers, subreddit, sort=sorting_method, time_filter=time_filter, limit=100, after=after)
                    # Add the delay to manage a rate of calls to the API.
                    time.sleep(3)
                    if response_json:
                        posts = extract_post_data(response_json)
                        after = response_json['data'].get('after')  # update 'after' token for pagination

                        if not posts:  # break if no new posts are fetched
                            print(f"No more posts to fetch from {subreddit}.")
                            break

                        for post in posts:
                            if post['post_id'] not in post_ids:
                                all_posts.append(post)
                                post_ids.add(post['post_id'])

                        print(f"Fetching posts from {subreddit} using {sorting_method} (Time: {time_filter}) (Total so far: {len(all_posts)}/{total_posts_per_subreddit})")

                        # break if 'after' token is None (no more pages to fetch)
                        if after is None:
                            break
                    else:
                        break
                except Exception as e:
                    print(f"An error occurred: {e}. Exiting...")
                    break

    # Return DataFrame
    df = pd.DataFrame(all_posts)
    return df

# main execution
def run_reddit_script():
    
    subreddit_1 = 'technology'
    subreddit_2 = 'gadgets'
    file_path = '../data/reddit_posts.csv'

    # define sorting methods and time filters
    sorting_methods = ['rising','hot', 'new', 'top','controversial']  
    time_filters = ['day', 'week', 'month', 'year', 'all']  # Relevant only for 'top' sorting method

    #  number of posts per subreddit
    total_posts_per_subreddit_1 = 3000  # For technology subreddit
    total_posts_per_subreddit_2 = 4000  # For gadgets subreddit

    #  Reddit data from subreddit 1
    new_posts_df_1 = fetch_reddit_data(client_id, client_secret, username, password, user_agent, subreddit_1, sorting_methods, time_filters, total_posts_per_subreddit_1)
    
    #  Reddit data from subreddit 2
    new_posts_df_2 = fetch_reddit_data(client_id, client_secret, username, password, user_agent, subreddit_2, sorting_methods, time_filters, total_posts_per_subreddit_2)

    # Combine the data from both subreddits
    new_posts_df = pd.concat([new_posts_df_1, new_posts_df_2], ignore_index=True)

    # Append to CSV or create if it doesn't exist
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        combined_df = pd.concat([existing_df, new_posts_df]).drop_duplicates(subset='post_id', keep='last')
    else:
        combined_df = new_posts_df

    combined_df.to_csv(file_path, index=False)
    print(f"New data has been appended to {file_path}")
# Run the script after every  six hour
if __name__ == '__main__':
    while True:
        run_reddit_script()  
        #time.sleep(6*3600)  # Wait for 6 hour 

