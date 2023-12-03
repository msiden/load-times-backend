# import db
import requests


def get_load_time(url: str, search_phrase) -> dict:

    if not url.startswith("http"):
        url = "http://" + url

    response = requests.get(url)
    response.raise_for_status()

    page_content = response.text.lower()

    return {
        "load_time": response.elapsed.total_seconds(),
        "search_phrase_occurencies": page_content.count(search_phrase.lower())
    }


def get_results() -> list:
    # return db.get_data(chunk_size, level)
    return [{"results": 1234}]

