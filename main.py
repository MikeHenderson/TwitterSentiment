from SentimentModel import SentimentModel
from TweetScraper import TweetScraper
import argparse
from typing import List
from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt


def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-username', help='Username to be searched on')
    parser.add_argument('-keyword', help='Keyword to be search on')
    parser.add_argument('-limit', help='Max number of results returned')
    parser.add_argument('-start', help='Beginning of search window')
    parser.add_argument('-end', help='Ending of search window')

    return parser.parse_args()


class Binning(Enum):
    WEEK = 0
    MONTH = 1


def presentation(keywords: List[str],
                 binning: Binning = Binning.WEEK, limit: int = 10000, start=None, end=None):

    scraper = TweetScraper()
    analyzer = SentimentModel()

    for keyword in keywords:
        scraper.searchByKeyword(keyword, limit, start, end)

        input_df = pd.read_csv('output.csv')
        results = []
        print("Starting classification of {}...".format(keyword))
        for index, row in input_df.iterrows():
            print("\r{}/{}".format(index, len(input_df)), end="")
            if analyzer.classify(row['tweet']):
                results.append((row['date'], 1, 0))
            else:
                results.append((row['date'], 0, -1))
        print("\nFinished...")

        results_df = pd.DataFrame(results, columns=['date', 'pos', 'neg'])
        results_df['date'] = pd.to_datetime(results_df['date'])
        if binning is Binning.WEEK:
            agg_df = results_df.groupby(pd.Grouper(key='date', freq='W')).sum()
        elif binning is Binning.MONTH:
            agg_df = results_df.groupby(pd.Grouper(key='date', freq='W')).sum()
        else:
            raise Exception("Binning type does not exist")

        fig, ax = plt.subplots()
        if binning is Binning.WEEK:
            width = 7
        elif binning is Binning.MONTH:
            width = 31
        else:
            raise Exception("Binning type does not exist")
        plt.bar(agg_df.index, agg_df['pos'], width=width, color='b')  # Width measured in days
        plt.bar(agg_df.index, agg_df['neg'], width=width, color='r')
        plt.title("Sentiment of {}".format(keyword))
        fig.autofmt_xdate()
        plt.savefig("{}.png".format(keyword), bbox_inches='tight')
        plt.show()


def cli():
    # py main.py --help for usage
    args = initArgs()

    if args.username and args.keyword:
        print('Support for username and keyword search together not available')

    scraper = TweetScraper()

    if args.username:
        scraper.searchByUsername(args.username, args.limit, args.start, args.end)
    elif args.keyword:
        scraper.searchByKeyword(args.keyword, args.limit, args.start, args.end)

    df = pd.read_csv('output.csv')
    analyzer = SentimentModel()

    result = []

    for index, row in df.iterrows():
        isPositive = analyzer.classify(row['tweet'])

        if isPositive:
            score = 1
        else:
            score = -1

        result.append((row['date'], score))

    resultDf = pd.DataFrame(result, columns=['date', 'positivity_score'])
    resultDf['date'] = pd.to_datetime(resultDf['date'])

    aggDf = resultDf.groupby(pd.Grouper(key='date', freq='W')).sum()

    if args.username:
        plt.title(f'Overall Sentiment for User @{args.username}')
    else:
        plt.title(f'Overall Sentiment for keyword {args.keyword}')

    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.plot(aggDf)
    plt.show()


if __name__ == '__main__':
    # cli()
    presentation(["discord", "imac", "tesla"])
