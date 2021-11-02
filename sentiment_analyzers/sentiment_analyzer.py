from fastapi import FastAPI
from pydantic import BaseModel
from typing import Tuple, List
import logging
from nltk.sentiment import SentimentIntensityAnalyzer

sentiment_intensity_analyzer = SentimentIntensityAnalyzer()

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(module)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

app = FastAPI()

class SentimentOfText(BaseModel):
    text: list

def get_sentiment_and_polarity_score(text:str)-> Tuple[dict,dict]:
    """Return a dict of polarity_score and final Sentiment"""
    scores = sentiment_intensity_analyzer.polarity_scores(text)
    senti = "Positive" if scores.get("compound")>=0.05 else "Negative" \
             if scores.get("compound")<=-0.05 else "Neutral"
    return scores,{"sentiment":senti}

@app.get("/test")
def test_route():
    """A route to test the working of the app"""
    return {"message":"The app is working!!"}

@app.post("/sentiment-of-text")
def texts_sentiment(sentiment_of_text:SentimentOfText):
    """
    A route to post list of text and get 
    polarity and sentiment of text
    """
    return_dict={}
    for text_ in sentiment_of_text.text:
        return_dict.update({text_:get_sentiment_and_polarity_score(text_)})
    return return_dict

if __name__ == "__main__":
    pass