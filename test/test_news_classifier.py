from unittest import TestCase

from news_classifier.news_classifier import BbcNewsClassifier, NewsCategoryClassifier
from topic_classifier.topic_classifiers import WebSiteClassifier, TopicClassification, ArkViClassifier
from financial_classifier.financial_news_classifier import EconomicsClassifier, FinancialNewsClassifier


class TestBbcNewsClassifier(TestCase):
    def test_classify_news_item(self):
        news_classifier = BbcNewsClassifier(classification_threshold=0.0)
        classified = news_classifier.classify_item("hello this is the news")
        print(classified)
        assert classified

        news_classifier = NewsCategoryClassifier(classification_threshold=0.0)
        classified = news_classifier.classify_item("hello this is the news")
        print(classified)
        assert classified

        news_classifier = EconomicsClassifier(classification_threshold=0.0)
        classified = news_classifier.classify_item("hello this is the news")
        print(classified)
        assert classified

        news_classifier = FinancialNewsClassifier(classification_threshold=0.0)
        classified = news_classifier.classify_item("hello this is the news")
        print(classified)
        assert classified

        topic_model = ArkViClassifier(classification_threshold=0.0)
        classified = topic_model.classify_item('hello this is the news')
        print(classified)
        assert classified

        topic_model = TopicClassification(classification_threshold=0.0)
        classified = topic_model.classify_item('hello this is the news')
        print(classified)
        assert classified


        topic_model = WebSiteClassifier(classification_threshold=0.0)
        classified = topic_model.classify_item('hello this is the news')
        print(classified)
        assert classified

