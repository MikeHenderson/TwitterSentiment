from SentimentModel import SentimentModel
from TweetScraper import TweetScraper
import argparse
import pandas as pd


def initArgs():
    parser = argparse.ArgumentParser();
    parser.add_argument('-username', help='Username to be searched on')
    parser.add_argument('-keyword', help='Keyword to be search on')
    parser.add_argument('-limit', help='Max number of results returned')
    parser.add_argument('-start', help='Beginning of search window')
    parser.add_argument('-end', help='Ending of search window')

    return parser.parse_args()


if __name__ == '__main__':
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
        result.append((row['tweet'], row['date'], isPositive))

    resultDf = pd.DataFrame(result, columns=['Tweet', 'Date', 'IsPositive'])

    print(resultDf)