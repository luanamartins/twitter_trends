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



def query_trends():
    trends = api.GetTrendsWoeid(woeid)
    prefix_size = len('https://twitter.com/search')
    # query_example = 'q=twitter%20&result_type=recent&since=2014-07-19&count=100'

    results = []
    for trend in trends:
        query = trend.url
        query = query[prefix_size:]
        query = query + '&result_type=recent&count=10'
        print(query)
        tweets = api.GetSearch(raw_query=query)
        accounts = []
        for tweet in tweets:
            accounts.append(tweet.user.screen_name)
        results.append(accounts)

    return results



def bot_classifier(results, twitter_app_auth):
    bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=s.rapidapi_key, **twitter_app_auth)
    for account in results:
        name = '@' + account.user.screen_name
        bom_score = bom.check_account(name)
        score = bom_score["display_scores"]["universal"]
        print(name + ' ' + str(score))


results = query_trends()
print(results)
