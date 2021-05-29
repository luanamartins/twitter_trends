import settings as s
import twitter
import json
import sys
import yweather
import botometer
import csv

from argparse import ArgumentParser


threshold = 0.6

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
    trends = api.GetTrendsCurrent()
    trends = trends[:1]
    results = []

    for trend in trends:
        query = trend.query
        query = 'q=' + query + '&result_type=recent&count=1'
        tweets = api.GetSearch(raw_query=query)

        for tweet in tweets:
            results.append({ 
                'trend': trend.name,
                'time': trend.timestamp,
                'username': tweet.user.screen_name,
                'is_bot': bot_classifier(tweet.user.screen_name)
            })

    return results


def write_csv(data):
    fnames = ['trend', 'time', 'username', 'is_bot']
    output_file = open('output.csv', 'w', newline='')
    writer = csv.DictWriter(output_file, fieldnames=fnames)

    with output_file:
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def bot_classifier(username):
    bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=s.rapidapi_key, **twitter_app_auth)
    account = '@' + username
    bot_score = bom.check_account(account)
    score = bot_score["display_scores"]["universal"]
    return score > threshold


if __name__ == "__main__":
    results = query_trends()
    write_csv(results)
