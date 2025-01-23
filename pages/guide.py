import streamlit as st
import pandas as pd

st.title("Guide")

st.write(
    '''Under the Data section on the sidebar on the left are all the tools that allow 
    you to download the csv file, Facebook and Instagram both export all the posts in 
    the specified month, and giveaways only works on instagram posts. '''
)

st.write(
    '''To use the tools under Data, you will need to have access to DANAMIC's API app. 
    You can click the button, Graph API Explorer, below to access it. '''
)

st.link_button('Graph API Explorer', url = 'https://developers.facebook.com/tools/explorer/')

st.write(
    '''Ensure that under permissions, you have the following (to add permissions, just click on add permissions and key in the permission name):'''
)

st.write(
    pd.DataFrame(
        {
            "Permissions" : ["read_insights", "pages_show_list", "ads_management", "ads_read", "business_management","instagram_basic", "instagram_manage_comments", "instagram_manage_insights", "pages_read_engagement", "pages_read_user_content"]
        }
    )
)

st.image('assets/Permissions.png', caption = 'How the permissions should look like (this is not all)')

st.write(
    '''For all the downloaded CSV files, either open in Google Sheets or Excel, but when opening with Excel, navigate to the data tab above, 
    then on the top left, click on "From Text/CSV", and reopen the file from there.'''
)

st.write('Expand to find out more.')

with st.expander("Facebook", icon = ":material/elderly:"):
    st.write(
        '''Do note check the engagement metrics with Meta Business Suite, there weren't any limitations specified by Meta, 
        but there may be some errors from time to time. The reach and impressions portion should be fine.'''
    )

    st.write(
        '''To use this, go to Meta Business Suite and find the Facebook account ID, you can find it by 
        clicking the settings button at the bottom left amd navigating to Pages under Accounts. 
        Then paste the account ID in the box that says, Account ID. As for acccount name, just put the name of the account'''
    )

    st.image('assets/FB_Acc_ID.png', caption = 'settings - bottom left, Pages - under Accounts, ID - under the name of the account')

    st.write(
        '''For the Date box, just put in the desired year and month, e.g. 2025-01'''
    )

    st.write(
        '''To get the page access token, go to the Graph API Explorer, make sure that under the "User or Page" section, it is the name of the 
        Facebook page you want to get the data of, e.g. when getting the data for DANAMIC FB page, it should say DANAMIC. Click on the 
        Copy Token button on the right of the access token (the long string of characters)'''
    )

    st.image('assets/Page_Access_Token.png', caption = 'Access token is on the top right, make sure to select the correct account')

    st.write(
        '''Once you have gotten the access token, paste it into the box that says, Page Access Token. Then click on the button, Get Data.'''
    )

    st.write(
        '''A success message should pop up along with a Download CSV button, click on it to download the CSV file.'''
    )

with st.expander("Instagram", icon = ":material/falling:"):
    st.write(
        '''Do note that due to Meta's limitations, the retrieved data will only be organic data.'''
    )

    st.write(
        '''To use this, go to Meta Business Suite and find the Instagram account ID, you can find it by 
        clicking the settings button at the bottom left amd navigating to Instagram Accounts under Accounts. 
        Then paste the account ID in the box that says, Account ID. As for acccount name, just put the name of the account'''
    )

    st.image('assets/IG_Acc_ID.png', caption = 'settings - bottom left, Instagram Accounts - under Accounts, ID - under the name of the account')

    st.write(
        '''For the Date box, just put in the desired year and month, e.g. 2025-01'''
    )

    st.write(
        '''To get the user access token, go to the Graph API Explorer, make sure that under the "User or Page" section, it is "User Token".
        Click on the Copy Token button on the right of the access token (the long string of characters)'''
    )

    st.image('assets/User_Access_Token.png', caption = 'Access token is on the top right')

    st.write(
        '''Once you have gotten the access token, paste it into the box that says, User Access Token. Then click on the button, Get Data.'''
    )

    st.write(
        '''A success message should pop up along with a Download CSV button, click on it to download the CSV file.'''
    )

with st.expander("Giveaway", icon = ":material/featured_seasonal_and_gifts:"):
    st.write(
        '''Do note that due to Meta's limitations, some of the comments will be left out - 
        Meta can only retrieve organic info for Instagram (should only be a few comments). 
        Recommended to check through with the comments on the post.'''
    )
    
    st.write(
        '''To use this, go to Meta Business Suite and find the giveaway post to get the 
        post ID. Then paste the post ID in the box that says, Post ID. As for the 
        giveaway name, just put the name of the giveaway.'''
    )

    st.link_button('Meta Business Suite', url = 'https://www.facebook.com/business/tools/meta-business-suite')

    st.image('assets/Giveaway_ID.png', caption = 'ID can be found below the date')

    st.write(
        '''To get the user access token, go to the Graph API Explorer, make sure that under the "User or Page" section, it is "User Token".
        Click on the Copy Token button on the right of the access token (the long string of characters)'''
    )

    st.image('assets/User_Access_Token.png', caption = 'Access token is on the top right')

    st.write(
        '''Once you have gotten the access token, paste it into the box that says, User Access Token. Then click on the button, Get Data.'''
    )

    st.write(
        '''A success message should pop up along with a Download CSV button, click on it to download the CSV file.'''
    )

with st.expander("Scraper", icon = ":material/preview:"):
    st.write(
        '''This scraper does not work on any pages that require CAPTCHA 
        or has a login prompt. Which means it does not work on any social media
        pages (IG, FB, TT). Works on pages that do not require CAPTCHA or login.'''
    )

    st.write(
        '''To use this, simply copy the URL of the desired website, and paste it into 
        the box provided and click on the button, Scrape Site. A preview of the website 
        should pop up, leave it be, it will auto close in a bit. '''
    )

    st.image('assets/Scraper_URL.png', caption = 'Box to paste URL')

    st.write(
        '''After which, a new text box along with a tab for you to 
        expand and see the content retrieved should appear. Type in the new box below 
        how you would like to see the data, for instance, you can ask for it to 
        phrase the data in a table, recommended to include your desired columns. 
        Then click on the button, Generate.'''
    )

    st.write(
        '''Note: this could take awhile.'''
    )

    st.image('assets/Scraper_LLM.png', caption = 'Box to type the desired output')


