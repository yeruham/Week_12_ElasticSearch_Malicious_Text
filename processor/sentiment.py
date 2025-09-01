import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

class Sentiment:


    @staticmethod
    def find_sentiment(text):
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        if score["compound"] > 0.5:
            sentiment = "positive"
        elif score["compound"] <= -0.50:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return sentiment
