import argparse
import os
import requests
import re
from bs4 import BeautifulSoup


def make_filename(url, type='html'):
    name = re.search(r'https?://(.*)', url).group(1)
    if type == 'html':
        name = re.sub(r'\W', '-', name) + '.html'
    elif type == 'dir':
        name = re.sub(r'\W', '-', name) + '_files'
    elif type == 'resource':
        extention = re.search(r'.*\.(.*)$', name).group(1)
        name = re.sub(f'\.{extention}$', '', name)
        name = re.sub(r'\W', '-', name)
    return name


def download(url, directory):
    r = requests.get(url)
    output_file = os.path.join(directory, make_filename(url))
    with open(output_file, 'w') as f:
        f.write(r.text)
    download_resources(url, directory)
    return output_file


def download_resources(url, directory):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for img in soup.find_all('img'):
        link = img.get('src')
        if is_relative_link(link):
            link = absolute_link(link, get_domain(url))
        if is_subdomain(url, link):
            if not os.path.exists(os.path.join(directory,
                                               make_filename(url, type='dir'))):
                os.makedirs(os.path.join(directory,
                                         make_filename(url, type='dir')))
            image_file_path = os.path.join(directory,
                                           make_filename(url, type='dir'),
                                           make_filename(link, type='resource'))
            with open(image_file_path, 'wb') as image_file:
                image_file.write(requests.get(link).content)


def is_subdomain(url1, url2):
    if get_domain(url1) in get_domain(url2):
        return True


def get_domain(url):
    try:
        domain = re.search(r'(?:https?:)?//(.*?)/', url).group(1)
    except AttributeError:
        return None
    return domain


def is_relative_link(link):
    search = re.search(r'^/[^/].*', link)
    return True if search else False


def absolute_link(relative_link, domain):
    return f'http://{domain}{relative_link}'


def is_invalid_url(url):
    try:
        re.search(r'https?://(.*)', url).group(1)
        return 0
    except AttributeError:
        print('URL is incorrect. Please check')
        return 1


def main():
    parser = argparse.ArgumentParser(description='Download page to file')
    parser.add_argument('url')
    parser.add_argument("-o", "--output",
                        default=os.getcwd(),
                        help="Destination directory")
    args = parser.parse_args()
    if not is_invalid_url(args.url):
        print(download(args.url, args.output))
    else:
        print('URL is not valid')


if __name__ == '__main__':
    main()
