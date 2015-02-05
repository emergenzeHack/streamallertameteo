import sys
import tweepy
import webbrowser
import sqlite3 as lite

# Query terms



sqlite3file='stream_meteo_user.sqlite'

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

con = lite.connect(sqlite3file)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS TWEETS(txt text, author text, created int, source text, id_str text,retweet_count text,favorite text)")

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        try:
           
            cur.execute("INSERT INTO TWEETS VALUES(?,?,?,?,?,?,?)", (status.text, status.author.screen_name, status.created_at, status.source,status.id_str,str(status.retweet_count),str(status.favorited)))
            con.commit()

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

follow_meteo=[
'407883178', '288736701', '2401221331' '636826547', '1055333070'
 '344612100', '227261658', '1263976393' '348688697', '97286264'  
'491603569', '263655940', '54717228'   '50396227'   '281944676' 
'355322650', '335226091', '185784926', '171392887', '43299072'  
'319027480', '104118823', '1062987055' '1876441272' '1139402323'
 '294604699', '44995834'   '334518857', '384797076', '185722558' 
 '1104732662' '1068581485' '571999691', '926156994', '72845881'  
 '84568718'   '568104607', '563573329', '491366686', '71230076'  
 '458173253', '2409481086' '196705620', '2408626556' '363180418' 
 '542677731', '1595473748' '279071701', '2197887554' '1923017286'
 '1156419355' '975805754', '608017592', '421101462', '485137607' 
 '734459096', '69238668'   '140886662', '1320033764' '372697410' 
 '263372828', '855357384', '52722712'   '401409503', '1384973898'
 '769451000', '209276057', '208731918', '18133268']	

			 
streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)

print >> sys.stderr, 'Filtering the public timeline for "%s\n"' % (' '.join(follow_meteo),)

streaming_api.filter(follow=follow_meteo)