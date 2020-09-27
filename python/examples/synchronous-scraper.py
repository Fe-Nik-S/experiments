
from urllib.request import Request, urlopen
from time import time


SITES = [
    "http://news.ycombinator.com/",
    "https://www.yahoo.com/",
    "http://salmonofcapistrano.com/",
    "https://mail.ru/"
]


def find_size(url):
    req = Request(url)
    with urlopen(req) as response:
        page = response.read()
    return len(page)


def main():
    for site in SITES:
        start_time = time()
        size = find_size(site)
        print("Read {:8d} chars from {} in {:6.3f} secs".format(size, site, time() - start_time))


if __name__ == '__main__':
    start_time = time()
    print("Start executing...")
    main()
    print("Ran in {:6.3f} secs".format(time() - start_time))
    print("End executing...")
