# Fintech Review Analytics

## Task 1: Data Collection & Preprocessing

### Scraping Methodology
- **Library**: `google-play-scraper` (Python)
- **Apps Scraped**: 
  - CBE Mobile (`com.combanketh.mobilebanking`)
  - BoA Mobile (`com.boa.boaMobileBanking`)
  - Dashen Mobile (`com.dashen.dashensuperapp`)
- **Fields Collected**: review text, review ID, rating (1-5), review date, bank name, source
- **Date Range**: Most recent 500 reviews per app (sorted by newest)
- **Language**: English (`lang='en'`)
- **Country**: Ethiopia (`country='et'`)

### Preprocessing Steps
1. **Duplicate Removal**: Deduplicated using `review_id + review + date` hash
2. **Missing Values**: Dropped rows missing review text or rating; documented counts
3. **Text Cleaning**: Collapsed whitespace, stripped edges, removed empty reviews post-cleaning
4. **Rating Validation**: Ensured all ratings are integers 1-5; removed out-of-range values
5. **Date Normalization**: Converted to `YYYY-MM-DD` format

### Data Quality
- **Total Reviews**: 1,500
- **Per Bank**: CBE [500], BoA [500], Dashen [500]
- **Missing Data Rate**: &lt;0%

### Limitations
- Google Play scraper may return fewer than 500 reviews if app has limited recent English reviews
- Review IDs are not always provided by the API; content-based deduplication used as fallback
- Date range is "most recent" rather than a fixed historical window