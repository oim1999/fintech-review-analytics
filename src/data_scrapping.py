# data_scrapping.py — FIXED VERSION
import pandas as pd
import re
from google_play_scraper import reviews, Sort

APPS = {
    'CBE Mobile':  'com.combanketh.mobilebanking',
    'BoA Mobile': 'com.boa.boaMobileBanking',
    'Dashen Mobile': 'com.dashen.dashensuperapp',
}


def scrape_fintech_reviews(app_dict, count=500, return_raw=False):
    """Fetches reviews for Ethiopian fintech apps from Google Play."""
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
                    'review_id': response.get('reviewId', ''),  # .get() for safety
                    'app': name,
                    'review': response.get('content', ''),
                    'rating': response.get('score', None),
                    'date': response.get('at', None),
                    'thumbs': response.get('thumbsUpCount', 0),
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
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text).lower())  # convert to lowercase and remove special characters
    text = text.strip()               # remove leading/trailing whitespace
    return text
