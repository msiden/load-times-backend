import db
import requests
from datetime import datetime


def get_load_time(url: str, search_phrase) -> dict:

    if not url.startswith("http"):
        url = "http://" + url

    now = str(datetime.now())

    response = requests.get(url)
    response.raise_for_status()

    page_content = response.text.lower()

    results = {
        "url": url,
        "search_phrase": search_phrase,
        "response_time": response.elapsed.total_seconds(),
        "occurencies": page_content.count(search_phrase.lower()),
        "start_time": now
    }

    db.insert_data(**results)

    return results


def get_results(chunk_size) -> list:
    return db.get_data(chunk_size)


