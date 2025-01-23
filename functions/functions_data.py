import re
import requests
import csv
import pandas
from io import StringIO

def is_valid_date(date):
    # Basic regex pattern for YYYY-MM format validation
    date_pattern = r"^\d{4}-(0[1-9]|1[0-2])$"
    return re.match(date_pattern, date) is not None

def is_fully_numeric(accid):
    # Check if the accid is fully numerical
    return accid.isdigit()

def get_fb_page_data(pageid, date, page_access_token):
    feed_url = f"https://graph.facebook.com/v20.0/{pageid}/feed?fields=id%2Cmessage%2Ccreated_time%2Cstatus_type%2Cpermalink_url%2Cshares%2Cfull_picture&access_token={page_access_token}"
    
    response_feed = requests.get(feed_url).json()

    posts = []
    
    loop = True
    
    while loop:
        for post in response_feed['data']:
            
            if post['created_time'].split('T')[0].startswith(date):
                post['id'] = post['id'].split('_')[-1]
                
                if 'shares' in post.keys():
                    post['shares'] = post['shares']['count']
                else:
                    post['shares'] = 0
                    
                if 'full_picture' not in post.keys():
                    post['full_picture'] = ''
                    
                if 'message' not in post.keys():
                    post['message'] = ''
                    
                comments_url = f"https://graph.facebook.com/v20.0/{pageid}_{post['id']}/comments?access_token={page_access_token}"
                
                response_comments = requests.get(comments_url).json()
                while True:
                    if 'data' in response_comments.keys():
                        post['comments'] = len(response_comments['data'])
                    else:
                        post['comments'] = 0
                        break
                        
                    if ('paging' in response_comments) and ('next' in response_comments['paging']):
                            next_page_url = f"https://graph.facebook.com/v20.0/{pageid}_{post['id']}/comments?pretty=0&limit=25&after={response_feed['paging']['cursors']['after']}&access_token={page_access_token}"
                            response_comments = requests.get(next_page_url).json()
                    else:
                        break
                
                posts.append(post)
            else:
                if len(posts) != 0:
                    loop = False
                continue
                
        # Check if there is a next page
        if ('paging' in response_feed) and ('next' in response_feed['paging']):
            next_page_url = f"https://graph.facebook.com/v20.0/{pageid}/feed?fields=id%2Cmessage%2Ccreated_time%2Cstatus_type%2Cpermalink_url%2Cshares&pretty=0&limit=25&after={response_feed['paging']['cursors']['after']}&access_token={page_access_token}"
            response_feed = requests.get(next_page_url).json()
        else:
            break
                
    for post in posts:
        temp_dict = {}
        
        postid = post['id']
        
        insights_url = f"https://graph.facebook.com/v20.0/{pageid}_{postid}/insights?metric=post_impressions%2Cpost_impressions_paid%2Cpost_impressions_unique%2Cpost_impressions_paid_unique%2Cpost_reactions_by_type_total%2Cpost_clicks_by_type&access_token={page_access_token}"
        
        response_insights = requests.get(insights_url).json()
        
        for metric in response_insights['data']:
            temp_dict[metric['name']] = metric['values'][0]['value']
            
        if 'post_impressions_paid' not in temp_dict.keys():
            temp_dict['post_impressions_paid'] = 0

        if 'post_impressions_paid_unique' not in temp_dict.keys():
            temp_dict['post_impressions_paid_unique'] = 0

        if 'post_reactions_by_type_total' not in temp_dict.keys():
            temp_dict['post_reactions_by_type_total'] = {'likes' : 0, 'love' : 0, 'wow' : 0, 'haha' : 0, 'sorry' : 0, 'anger' : 0, }

        if 'post_clicks_by_type' not in temp_dict.keys():
            temp_dict['post_clicks_by_type'] = {'other clicks' : 0, 'photo clicks' : 0, 'link clicks' : 0}

        if 'likes' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['likes'] = 0

        if 'love' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['love'] = 0

        if 'wow' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['wow'] = 0

        if 'haha' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['haha'] = 0

        if 'sorry' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['sorry'] = 0

        if 'anger' not in temp_dict['post_reactions_by_type_total'].keys():
            temp_dict['post_reactions_by_type_total']['anger'] = 0

        if 'other clicks' not in temp_dict['post_clicks_by_type'].keys():
            temp_dict['post_clicks_by_type']['other clicks'] = 0

        if 'photo clicks' not in temp_dict['post_clicks_by_type'].keys():
            temp_dict['post_clicks_by_type']['photo clicks'] = 0

        if 'link clicks' not in temp_dict['post_clicks_by_type'].keys():
            temp_dict['post_clicks_by_type']['link clicks'] = 0
                
        temp_dict['post_reactions_by_type_total']['total'] = (temp_dict['post_reactions_by_type_total']['likes'] + temp_dict['post_reactions_by_type_total']['love'] + temp_dict['post_reactions_by_type_total']['wow'] + temp_dict['post_reactions_by_type_total']['haha'] + temp_dict['post_reactions_by_type_total']['sorry'] + temp_dict['post_reactions_by_type_total']['anger'])
                
        temp_dict['post_clicks_by_type']['total'] = (temp_dict['post_clicks_by_type']['other clicks'] + temp_dict['post_clicks_by_type']['photo clicks'] + temp_dict['post_clicks_by_type']['link clicks'])
        
        temp_dict['engagements'] = (temp_dict['post_reactions_by_type_total']['total'] + post['comments'] + post['shares'])

        if temp_dict['post_impressions_unique'] != 0:
            temp_dict['engagement_rate'] = temp_dict['engagements'] / temp_dict['post_impressions_unique']

        else:
            temp_dict['engagement_rate'] = 0

        post['insights'] = temp_dict
    
    # Create CSV in-memory
    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Post ID', 'Picture URL', 'Message', 'Created Time', 'Status Type', 'Permalink', 'Comments', 'Shares', 
                     'Impressions', 'Impressions - Paid', 'Reach', 'Reach - Paid', 'Total Reactions', 'Likes', 'Love', 
                     'Wow', 'Haha', 'Sorry', 'Anger', 'Total Clicks', 'Other Clicks', 'Photo Clicks', 'Link Clicks', 
                     'Engagements', 'Engagement Rate'])
    
    for post in posts:
        insights = post['insights']
        writer.writerow([post['id'], post['full_picture'], post['message'], post['created_time'], post['status_type'], 
                         post['permalink_url'], post['comments'], post['shares'], insights.get('post_impressions', 0), 
                         insights.get('post_impressions_paid', 0), insights.get('post_impressions_unique', 0), 
                         insights.get('post_impressions_paid_unique', 0), insights['post_reactions_by_type_total']['total'], 
                         insights['post_reactions_by_type_total']['likes'], insights['post_reactions_by_type_total']['love'], 
                         insights['post_reactions_by_type_total']['wow'], insights['post_reactions_by_type_total']['haha'], 
                         insights['post_reactions_by_type_total']['sorry'], insights['post_reactions_by_type_total']['anger'], 
                         insights['post_clicks_by_type']['total'], insights['post_clicks_by_type']['other clicks'], 
                         insights['post_clicks_by_type']['photo clicks'], insights['post_clicks_by_type']['link clicks'], 
                         insights['engagements'], insights['engagement_rate']])
    
    output.seek(0)  # Reset the buffer position for reading
    return output

def get_insta_page_data(accountid, date, user_access_token):
    url = f"https://graph.facebook.com/v20.0/{accountid}/media?fields=id%2Ccaption%2Ctimestamp%2Cmedia_type%2Cpermalink%2Cmedia_url&access_token={user_access_token}"
    
    response_media = requests.get(url).json()
    
    posts = []
    
    loop = True
    
    while loop:
        for post in response_media['data']:
            if post['timestamp'].split('T')[0].startswith(date):

                if 'media_url' not in post.keys():
                    post['media_url'] = ''

                posts.append(post)
            else:
                if len(posts) != 0:
                    loop = False
                continue
  
        # Check if there is a next page
        if ('paging' in response_media) and ('after' in response_media['paging']['cursors']):
            next_page_url = f"https://graph.facebook.com/v20.0/{accountid}/media?fields=id%2Ccaption%2Ctimestamp%2Cmedia_type%2Cpermalink&pretty=0&limit=25&after={response_media['paging']['cursors']['after']}&access_token={user_access_token}"
            response_media = requests.get(next_page_url).json()
        else:
            break
            
    for post in posts:
        postid = post['id']
        
        if post['media_type'] in ['CAROUSEL_ALBUM', 'IMAGE']:
            post_url = f"https://graph.facebook.com/v20.0/{postid}/insights?metric=impressions%2Creach%2Clikes%2Ccomments%2Cshares%2Csaved%2Ctotal_interactions%2Cprofile_visits%2Cprofile_activity&access_token={user_access_token}"
            
        elif post['media_type'] in ['VIDEO']:
            post_url = f"https://graph.facebook.com/v20.0/{postid}/insights?metric=plays%2Creach%2Clikes%2Ccomments%2Cshares%2Csaved%2Ctotal_interactions%2Cig_reels_avg_watch_time%2Cig_reels_video_view_total_time&access_token={user_access_token}"

        response_post = requests.get(post_url).json()

        temp_dict = {}

        for metric in response_post['data']:
            temp_dict[metric['name']] = metric['values'][0]['value']

        temp_dict['engagements'] = (temp_dict['likes'] + temp_dict['comments'] + temp_dict['shares'] + temp_dict['saved'])
        
        if temp_dict['reach'] != 0:
            temp_dict['engagement_rate'] = temp_dict['engagements'] / temp_dict['reach']
            
        else:
            temp_dict['engagement_rate'] = 0
        
        post['insights'] = temp_dict
    
    # Create CSV in-memory
    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Post ID', 'Picture URL', 'Picture', 'Caption', 'Timestamp', 'Media Type', 'Permalink', 'Impressions', 'Plays', 'Reach', 
                     'Likes', 'Comments', 'Shares', 'Saved', 'Total Interactions', 'Profile Visits', 'Profile Activity', 
                     'Avg Watch Time', 'Total Watch Time', 'Engagements', 'Engagement Rate'])

    for dict in posts:
        insights = dict['insights']
        if dict['media_type'] in ['CAROUSEL_ALBUM', 'IMAGE']:
            writer.writerow([str(dict['id']), str(dict['media_url']), '', str(dict['caption']), str(dict['timestamp']), str(dict['media_type']), 
                             str(dict['permalink']), str(insights['impressions']), '', str(insights['reach']), 
                             str(insights['likes']), str(insights['comments']), str(insights['shares']), 
                             str(insights['saved']), str(insights['total_interactions']), str(insights['profile_visits']), 
                             str(insights['profile_activity']), '', '', str(insights['engagements']), str(insights['engagement_rate'])])
                             
        elif dict['media_type'] in ['VIDEO']:
            writer.writerow([str(dict['id']), '', '', str(dict['caption']), str(dict['timestamp']), str(dict['media_type']), 
                             str(dict['permalink']), '', str(insights['plays']), str(insights['reach']), 
                             str(insights['likes']), str(insights['comments']), str(insights['shares']), 
                             str(insights['saved']), str(insights['total_interactions']), '', '', 
                             str(insights['ig_reels_avg_watch_time']), str(insights['ig_reels_video_view_total_time']), 
                             str(insights['engagements']), str(insights['engagement_rate'])])

    output.seek(0)  # Reset the buffer position for reading
    return output

def get_insta_post(postid, user_access_token):
    url = f"https://graph.facebook.com/v20.0/{postid}/comments?fields=id%2Cusername%2Ctext%2Ctimestamp&access_token={user_access_token}"

    response_comments = requests.get(url).json()

    comments_data = []
    
    while True:
        for comment in response_comments['data']:
            comments_data.append(comment)

        # Check if there is a next page
        if ('paging' in response_comments) and ('after' in response_comments['paging']['cursors']):
            next_page_url = f"https://graph.facebook.com/v20.0/{postid}/comments?fields=id%2Cusername%2Ctext%2Ctimestamp&pretty=0&limit=25&after={response_comments['paging']['cursors']['after']}&access_token={user_access_token}"
            response_comments = requests.get(next_page_url).json()
        else:
            break

    # Create CSV in-memory
    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Username', 'Comment', 'Timestamp', 'Link'])
    for dict in comments_data:
        writer.writerow([str(dict['username']), str(dict['text']), str(dict['timestamp']), f"https://www.instagram.com/{str(dict['username'])}/"])

    output.seek(0)  # Reset the buffer position for reading
    return output

