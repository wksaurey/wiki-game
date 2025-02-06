import json
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'wksaurey@gmail.com'
}


def main():

    if len(sys.argv) > 1:
        title = sys.argv[1]
    else:
        title = get_random_title(headers)

    dest_title = 'Adolf_Hitler'

    paths = [[title]]

    max_path_length = 10

    print(search_for_path(title, dest_title, paths, max_path_length))


def search_for_path(source, dest_title, paths, max_path_length):
    print_status = False
    os.system('clear')
    print(f'Searching for {pretty_title(dest_title)} from {pretty_title(source)}...')
    while paths:
        path = paths.pop(0)
        title = path[-1]

        if title == dest_title:
            result = f'Found {pretty_title(dest_title)} from {pretty_title(source)} in {len(path)} links!'
            for title in path:
                result = result + (f'\n{pretty_title(title)}')
            return result

        if len(path) > max_path_length:
            return f'Unable to find {pretty_title(dest_title)} in {max_path_length} links.'

        html = get_html_from_title(title, headers)
        page_links = get_links_from_html(html)

        # print status
        if print_status:
            for _ in range(4):
                # cursor up one line
                sys.stdout.write('\x1b[1A')
                # delete last line
                sys.stdout.write('\x1b[2K')
        print(f'Current path length: {len(path)}')
        print(f'Number of paths to check: {len(paths)+1}')
        print(f'Current page: {title}')
        print_status = True
        print(f'Number of links on current page: {len(page_links)}')
        # time.sleep(.25)

        for link in page_links:
            link_title = link.strip('./')
            new_path = path.copy()
            new_path.append(link_title)
            paths.append(new_path)


def pretty_title(title):
    return title.replace('_', ' ')


def get_links_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    links = [a['href'] for p in soup.find_all('p') for a in soup.find_all('a', href=True)]
    links = list(filter(lambda link: link.startswith('./'), links))
    links = list(filter(lambda link: ':' not in link, links))
    links = list(filter(lambda link: '#' not in link, links))

    return links


def get_random_title(headers):
    random_title_url = 'https://en.wikipedia.org/api/rest_v1/page/random/title'
    response = requests.get(random_title_url, headers=headers)

    random_title = json.loads(response.content)["items"][0]["title"]

    return random_title


def get_html_from_title(title, headers):
    page_from_title_url = 'https://en.wikipedia.org/api/rest_v1/page/html/'
    page_url = page_from_title_url + title
    response = requests.get(page_url, headers=headers)

    html = response.content.decode('utf-8')

    return html


if __name__ == '__main__':
    main()
