import validators
import requests
from retry import retry

import extractor


def get_urls_from_file(path):
    with open(path) as f:
        urls = f.read().splitlines()
    urls = list(filter(validators.url, urls))
    return urls


@retry(tries=5, delay=2)
def fetch(url):
    print('Started downloading from : {}'.format(url))
    response = requests.get(url)
    content = str(response.content, 'UTF-8')
    print('Completed downloading from : {}'.format(url))
    return content


def fetch_urls(urls):
    contents = []
    for url in urls:
        try:
            content = fetch(url)
            contents.append(content)
        except:
            print(f'unable to fetch domains from: {url}')
    return contents


def load_domains_for_urls(urls):
    contents = fetch_urls(urls)
    res_domains = []
    for c in contents:
        domains = extractor.extract_domains(c)
        res_domains.extend(domains)

    return res_domains
