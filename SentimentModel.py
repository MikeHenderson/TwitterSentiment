import random
from typing import Tuple, List

import nltk
from nltk.corpus import twitter_samples, stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import classify
from nltk import NaiveBayesClassifier


class SentimentModel:

    def __init__(self):
        # Download package requirements
        nltk.download('twitter_samples')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')

        # training data
        self.positive_training_data = twitter_samples.strings('positive_tweets.json')
        self.negative_training_data = twitter_samples.strings('negative_tweets.json')

        # Save stopwords
        self.stopwords = stopwords.words('english')

        # Run self training
        self._train()

    @staticmethod
    def _to_lemmatize_pos(token: Tuple[str, str]) -> (str, str):
        word, tag = token
        if tag.startswith("NN"):
            return word, "n"
        elif tag.startswith("VB"):
            return word, "v"
        else:
            return word, "a"

    @staticmethod
    def _filter_tokens(token: Tuple[str, str]) -> bool:
        word, tag = token
        if "://t.co" in word:
            return False
        if word.startswith("#") or word.startswith("@"):
            return False
        return True

    def _preprocess_single(self, tweet: str) -> List[str]:
        # Split tweet into tokens
        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(tweet)

        # Tag each token
        tokens = [self._to_lemmatize_pos(x) for x in pos_tag(tokens) if self._filter_tokens(x)]
        # Lemmatize each token
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(x, y) for x, y in tokens]
        # Filter stopwords and lower
        words = [x.lower() for x in words if x not in self.stopwords]

        return words

    def preprocess(self, line) -> dict:
        output = {}
        for token in self._preprocess_single(line):
            output[token] = True
        return output

    # Returns True for positive tweet, False for negative tweet
    def classify(self, line) -> bool:
        return self.classifier.classify(self.preprocess(line))

    def _train(self):
        full_dataset = [(self.preprocess(x), True) for x in self.positive_training_data]
        full_dataset.extend([(self.preprocess(x), False) for x in self.negative_training_data])
        random.shuffle(full_dataset)

        train_data = full_dataset[:7000]
        test_data = full_dataset[7000:]

        self.classifier = NaiveBayesClassifier.train(train_data)
        print("Current accuracy to test data is: {}".format(classify.accuracy(self.classifier, test_data)))
        self.classifier.show_most_informative_features()