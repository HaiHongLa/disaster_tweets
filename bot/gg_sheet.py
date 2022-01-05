import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_file='core-site-329315-921d4cbc1452.json')

# # Create empty dataframe
# df = pd.DataFrame()

# # Create a column
# df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('DisasterTweets')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(df,(1,1))

# wks.sort_range('A2', 'A4', sortorder='DESCENDING')
wks.clear()

l = ['username', 'acctdesc', 'location', 'following',
    'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
    'retweetcount', 'text', 'hashtags']
wks.insert_rows(0, 3, l, False)
wks.insert_rows()