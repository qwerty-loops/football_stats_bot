import praw
import config
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
import time
import os

def bot_login():
    print ("Logging in...")
	
    r = praw.Reddit(
    client_id="7al91jG6vnSLT_9wunnRsw",
    client_secret="NgbJ60zbeM7pMQN1hv8EpXEakyeVHA",
    user_agent="<console:Football_Stats:1.0>",
    username = "Football_Stats_Bot",
    password = "footballstatsbot1"
        )

    return r

def run_bot(r, comments_replied_to):

    #Choose subreddit
    subreddit=r.subreddit("stats_bot")

    #Extracting Manchester United data from Fbref Premier League stats table
    
    print('Parsing through Fbref Stats page for Manchester United players')
    url = 'https://fbref.com/en/squads/19538871/Manchester-United-Stats#all_stats_standard'
    html_content = requests.get(url).text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    data = (df[0])

    data.columns = ['Player','Nation','Pos','Age','MP','Starts','Min','90s','Gls','Ast',
                'G-PK','PK','PKatt','CrdY','CrdR','Glsp90','Astp90','G+A','G-PK','G+A-PK',
                'xG','npxG','xA','npxG+xA','xGp90','xAp90','xG+xA','npxGp90','npxG+xAp90','Matches']


    data['Nation']=data['Nation'].str.split(' ',expand=True)[1]
    #data['Age']=data['Age'].str.split('-',expand=True)[1]
    data['Age']=data['Age'].astype(int)

    #Trying to drop nan records
    data.dropna()


    data=data.drop (['90s','G-PK','PK','PKatt','CrdY','CrdR','Glsp90','Astp90','G-PK','G+A-PK','xGp90','xAp90','xG+xA','npxGp90','npxG+xAp90','Matches'],axis=1)

    #Order by new/hot/top and display title of posts
    
    for post in subreddit.new(limit=20):
        for comment in post.comments:
            if hasattr(comment,"body"):
                comment_lower = comment.body.lower()
                if 'statsbot!' in comment_lower and comment.id not in comments_replied_to and comment.author != r.user.me():
                    print('--------------------------')
                    print(comment.body)
                    option = comment.body
                    choice = option.split('!',1)
                    if choice[0] == 'statsbot' or choice[0] == 'Statsbot' or choice[0]=='STATSBOT':
                        player =choice[1].title()
                        if player not in data.values:
                            
                            print ('Requested player does not play for Manchester United. Try again.')
                            comment.reply('Requested player does not play for Manchester United. Try again.')
                            comments_replied_to.append(comment.id)

                            with open ("comments_replied_to.txt", "a") as f:
                                f.write(comment.id + "\n")
                            break
                        dp = data[data['Player']== player]
                        dp=dp.drop(dp.columns[[3,5,6]],axis=1)
                        r='a|b|c|\n-|-|-\n1|2|3|\n4|5|6'
                        v1 =str(dp.iat[0,0])
                        v2=str(dp.iat[0,1])
                        v3=str(dp.iat[0,2])
                        v4=str(dp.iat[0,3])
                        v5=str(dp.iat[0,4])
                        v6=str(dp.iat[0,5])
                        v7=str(dp.iat[0,6])
                        v8=str(dp.iat[0,7])
                        v9=str(dp.iat[0,8])
                        v10=str(dp.iat[0,9])
                        v11=str(dp.iat[0,10])
                        v='Name'+'|'+'Nation'+'|'+'Position'+'|'+'MP'+'|'+'Gls'+'|'+'Asts'+'|'+'G+A'+'|'+'xG'+'|'+'npxG'+'|'+'xA'+'|'+'npxG+xA'+'\n'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'|'+'-'+'\n'+v1+'|'+v2+'|'+v3+'|'+v4+'|'+v5+'|'+v6+'|'+v7+'|'+v8+'|'+v9+'|'+v10+'|'+v11
                        print (dp)
                        #print (comment.refresh())
                        comment.reply(v)
                        print('--------------------------')
                
                        print ('Successfully replied to comment ',comment.id)
                        comments_replied_to.append(comment.id)

                        with open ("comments_replied_to.txt", "a") as f:
                            f.write(comment.id + "\n")

                    elif choice[0].lower != 'statsbot':
                        print ('Cannot process request')
                        #print ("Player does not exist/Request already commented to!")
                        break;

    print ("Search Completed.")
    print (comments_replied_to)

    print ("Sleeping for 30 seconds...")
    time.sleep(500)
    print ("###############################")
                    


def get_saved_comments():
    
    if not os.path.isfile("comments_replied_to.txt"):

        comments_replied_to = []
        
    else:
        
        with open("comments_replied_to.txt", "r") as f:
            
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to

r = bot_login() #goes to login function
comments_replied_to = get_saved_comments()#checks replied comments

print (comments_replied_to)

#Starts from here

while True:
    run_bot(r, comments_replied_to)
