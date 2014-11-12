import sys
import tweepy
import webbrowser
import sqlite3 as lite

# Query terms



sqlite3file='stream_allertameteo.sqlite'

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
            
            cur.execute("INSERT INTO TWEETS VALUES(?,?,?,?,?,?,?)", (status.text, status.author.screen_name, status.created_at, status.source,status.id_str,str(status.retweet_count),str(status.favorited),))
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

		


		
		
track_meteo=['#allertameteo','#allertameteoLIG',
	'#allertameteoTOS',
	'#allertameteoPM',
	'#allertameteoLAZ',
	'#allertameteoER',
	'#allertameteoMAR',
	'#allertameteoUM',
	'#allertameteoABR',
	'#allertameteoMOL',
	'#allertameteoCAM',
	'#allertameteoBAS',
	'#allertameteoPUG',
	'#allertameteoCAL',
	'#allertameteoSIC',
	'#allertameteoSAR',
	'#allertameteoLOM',
	'#allertameteoVEN',
	'#allertameteoTAA',
	'#allertameteoFVG',
	'#allertameteoTS']
			 
streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)

print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(track_meteo),)

streaming_api.filter( track=track_meteo,languages = ["it"])
