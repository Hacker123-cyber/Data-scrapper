from google_play_scraper import reviews, Sort
import pandas as pd
import os

def scrape_google_play_reviews(app_id, lang='en', country='us', count=100):
    reviews_data = []
    batches = count // 9000  # Determine the number of batches needed
    remainder = count % 9000  # Determine any remainder after full batches

    for i in range(batches):
        result, _ = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.MOST_RELEVANT,
            count=9000,
            filter_score_with=None,
            continuation_token=None if i == 0 else token  # Use token for pagination
        )
        reviews_data.extend(result)
        token = _  # Update the continuation token for pagination

    # Handle remaining reviews if count is not a multiple of 100
    if remainder > 0:
        result, _ = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.MOST_RELEVANT,
            count=remainder,
            filter_score_with=None,
            continuation_token=token  # Use token for pagination
        )
        reviews_data.extend(result)

    return reviews_data

def save_reviews_to_csv(reviews_data, file_name):
    df_reviews = pd.DataFrame(reviews_data)
    df_selected = df_reviews[['userName', 'score', 'at', 'content']]
    df_sorted = df_selected.sort_values(by='at', ascending=False)

    # Get the Downloads folder path
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder, file_name)

    df_sorted.to_csv(file_path, index=False)
    print(f"Scraped reviews data saved to: {file_path}")

if __name__ == "__main__":
    app_id = 'com.tokopedia.tkpd'  # Shopee app ID on Google Play
    reviews_count = 9000  # Number of reviews to scrape
    reviews_data = scrape_google_play_reviews(app_id, lang='id', country='id', count=reviews_count)
    csv_file_name = "scrapped_data.csv"
    save_reviews_to_csv(reviews_data, csv_file_name)