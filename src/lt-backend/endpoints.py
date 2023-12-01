# import db
import requests


def get_load_time(url: str) -> dict:
    response = requests.get(url)
    print(url, response.status_code, response.elapsed, type(response.elapsed))
    # print(response.text)
    return {"load_time": 1.00012}


def get_results() -> list:
    # return db.get_data(chunk_size, level)
    return [{"results": 1234}]

