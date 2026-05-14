import pandas as pd
import re
from google_play_scraper import app, reviews, Sort

APPS = {
    'CBE Mobile':  'com.combanketh.mobilebanking',
    'BoA Mobile': 'com.boa.boaMobileBanking',
    'Dashen Mobile': 'com.dashen.dashensuperapp',
}


def scrape_fintech_reviews(app_dict, count=500, return_raw=False):
    """Fetches 500 reviews for CBE, BoA and Dashen Mobile apps."""
    all_reviews = []
    for name, pkg in app_dict.items():
        try:
            responses, continuation_token = reviews(
                pkg,
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=count
            )
            if return_raw:
                return responses
            for response in responses:
                all_reviews.append({
                    'review_id': response['reviewId'],
                    'app': name,
                    'review': response['content'],
                    'rating': response['score'],
                    'date': response['at'],
                    'thumbs': response['thumbsUpCount'],
                    'bank': name,
                    'source': 'Google Play'
                })
            print(f"  Scraped {len(responses)} reviews for {name}")
        except Exception as e:
            print(f"  Failed to scrape {name}: {e}")
    return pd.DataFrame(all_reviews)

def clean_text(text):
    """Standardize review text: collapse whitespace, strip edges."""
    if pd.isna(text):
        return ''
    text = str(text)
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces/newlines
    text = text.strip()               # remove leading/trailing whitespace
    return text
