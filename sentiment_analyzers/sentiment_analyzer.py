from fastapi import FastAPI, UploadFile, File
from paramiko import file
from pydantic import BaseModel
from typing import Tuple, List
import logging
from nltk.sentiment import SentimentIntensityAnalyzer
import cv2
import numpy as np
from pydantic.utils import update_normalized_all
from PIL import Image
import io
import pytesseract
from concurrent.futures import ThreadPoolExecutor
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

sentiment_intensity_analyzer = SentimentIntensityAnalyzer()

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(module)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

app = FastAPI()


class SentimentOfText(BaseModel):
    text: list


def get_sentiment_and_polarity_score(text: str) -> Tuple[dict, dict]:
    """Return a dict of polarity_score and final Sentiment"""
    scores = sentiment_intensity_analyzer.polarity_scores(text)
    senti = "Positive" if scores.get("compound") >= 0.05 else "Negative" \
        if scores.get("compound") <= -0.05 else "Neutral"
    return {"text":text,"polarity_scores":scores, "sentiment": senti}


def get_sentiments_for_images(image) -> Tuple[dict, dict]:
    """Return a dict of polarity_score and final Sentiment for images"""
    img = Image.open(image)
    # img = cv2.imread(image)
    return get_sentiment_and_polarity_score(pytesseract.image_to_string(img).strip())


@app.get("/test")
def test_route():
    """A route to test the working of the app"""
    return {"message": "The app is working!!"}


@app.post("/sentiment-of-text")
def texts_sentiment(sentiment_of_text: SentimentOfText):
    """
    A route to post list of text and get 
    polarity and sentiment of text
    """
    with ThreadPoolExecutor(max_workers=2) as exe:
        logger.info(f"Working with texts")
        return_dict = exe.map(get_sentiment_and_polarity_score,sentiment_of_text.text)
    # for text_ in sentiment_of_text.text:
    #     return_dict.update({text_: get_sentiment_and_polarity_score(text_)})
    logger.info("Done with texts")
    return return_dict


@app.post("/sentiment-of-image")
def image_sentiment(image: UploadFile = File(...)):
    """
    A route to post image and get 
    polarity and sentiment of text
    """
    return {"file_name":f"{image.filename}", **get_sentiments_for_images(image.file)}

if __name__ == "__main__":
    pass
