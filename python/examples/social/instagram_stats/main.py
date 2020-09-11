
import requests
from bs4 import BeautifulSoup


BASE_URL_TEMPLATE = "https://www.instagram.com/{username}/"
DEFAULT_PARSER = "html.parser"
DEFAULT_PROPERTY = "og:description"
OUTPUT_TEMPLATE = "This account [@{username}] has '{count}' {property}"
PROPERTIES = [
    "followers",
    "following",
    "posts"
]


def parse_data(text):
    # text template: 163 Followers, 444 Following, 0 Posts - See Instagram photos and videos from
    parsed_data = text.split("-")[0]
    parsed_data = parsed_data.split(" ")
    user_info = [parsed_data[0], parsed_data[2], parsed_data[4]]
    return dict(
        zip(PROPERTIES, user_info)
    )


def scrape_data(user_name):
    full_url = BASE_URL_TEMPLATE.format(username=user_name)
    response = requests.get(full_url)
    if response.status_code == 404:
        raise Exception("User '{}' not found".format(user_name))
    if response.status_code != 200:
        raise Exception("Wrong response with '{}' code. Please repeat later...".format(response.status_code))
    metadata = BeautifulSoup(response.text, DEFAULT_PARSER).find("meta", property=DEFAULT_PROPERTY)
    return parse_data(metadata["content"])


if __name__ == "__main__":
    print("Please enter username:")
    username = input()
    userinfo = scrape_data(username)
    for prop in PROPERTIES:
        print(OUTPUT_TEMPLATE.format(username=username, count=userinfo[prop], property=prop))
