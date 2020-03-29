import settings as s
import twitter
import json
import yweather
import botometer

client = yweather.Client()
woeid = client.fetch_woeid('Brazil')

twitter_app_auth = {
    'consumer_key': s.consumer_key,
    'consumer_secret': s.consumer_secret,
    'access_token': s.access_token_key,
    'access_token_secret': s.access_token_secret,
}

api = twitter.Api(consumer_key=s.consumer_key,
                  consumer_secret=s.consumer_secret,
                  access_token_key=s.access_token_key,
                  access_token_secret=s.access_token_secret)

trends = api.GetTrendsWoeid(woeid)
first = trends[0]
query = first.url
prefix_size = len('https://twitter.com/search')
query = query[prefix_size:]
# query = query + '&count=100'
print(query)
query_example = "q=twitter%20&result_type=recent&since=2014-07-19&count=100"
results = api.GetSearch(raw_query=query)

account = results[0].user.screen_name
print(account)
bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=s.rapidapi_key, **twitter_app_auth)
response = bom.check_account(account)
score = response["display_scores"]["universal"]
print(score)
