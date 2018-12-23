from pathlib import Path
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup


def get_page(url):
    return requests(url)


def parse_page(page, base_url):
    links = []
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
        relative_link = to_relative(link.attrs['href'], base_url)
        if relative_link:
            link.attrs['href'] = relative_link
            links.append(relative_link) 
    return str(soup), links


def to_relative(url, base_url):
    parsed_url = urlsplit(url)
    parsed_base_url = urlsplit(base_url)
    if parsed_url.netloc and parsed_url.netloc != parsed_base_url.netloc:
        return None
    base_path = parsed_base_url.path.strip('/')
    path = parsed_url.path.strip('/')
    if path.startswith(base_path):
        return path[len(base_path):].strip('/')


def save_page(page, url, base_url, base_dir):
    page_path = to_relative(url, base_url)
    page_file = Path(base_dir).joinpath(page_path)
    page_file.parent.mkdir(parents=True, exist_ok=True)
    page_file.write_text(page)


def main():
    pass


if __name__ == "__main__":
    main()
