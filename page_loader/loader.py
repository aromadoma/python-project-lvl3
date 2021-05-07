import argparse
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse


def make_filename(url, type='html'):
    name = re.search(r'//(.*)', url).group(1)
    if type == 'html':
        name = re.sub(r'\W', '-', name) + '.html'
    elif type == 'dir':
        name = re.sub(r'\W', '-', name) + '_files'
    elif type == 'resource':
        extention = re.search(r'.*\.(.*)$', name).group(1)
        name = re.sub(fr'\.{extention}$', '', name)
        name = re.sub(r'\W', '-', name)
    return name


def create_dir(path, base_url):
    if not os.path.exists(os.path.join(path,
                                       make_filename(base_url, type='dir'))):
        os.makedirs(os.path.join(path, make_filename(base_url, type='dir')))


def download(base_url, path):
    """Download html document"""
    output_file = os.path.join(path, make_filename(base_url))
    with open(output_file, 'w') as f:
        f.write(download_resources(base_url, path))
    return output_file


def get_resource_url(tag):
    """Return URL from tag"""
    if tag.name in ['img', 'script']:
        return tag.get('src')
    if tag.name == 'link':
        return tag.get('href')


def download_resource(url):
    pass


def download_resources(base_url, path):
    """Download local resources and return updated html document"""
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for img in soup.find_all('img'):
        resource_url = absolute_url(base_url, get_resource_url(img))
        if is_subdomain(base_url, resource_url):
            create_dir(path, base_url)
            resource_file_path = os.path.join(path,
                                              make_filename(base_url,
                                                            type='dir'),
                                              make_filename(resource_url,
                                                            type='resource')
                                              )
            local_resource_path = os.path.join(make_filename(base_url,
                                                             type='dir'),
                                               make_filename(resource_url,
                                                             type='resource')
                                               )
            with open(resource_file_path, 'wb') as f:
                f.write(requests.get(resource_url).content)
            # Updating local resource's URL:
            img['src'] = local_resource_path

    return soup.prettify(formatter='html5')


def get_domain(url):
    return urlparse(url).netloc


def is_subdomain(url1, url2):
    if get_domain(url1) in get_domain(url2):
        return True


def is_relative_url(url):
    return True if not urlparse(url).netloc else False


def has_no_scheme(url):
    if not urlparse(url).scheme:
        return True


def absolute_url(base_url, url):
    if is_relative_url(url):
        return urljoin(base_url, url)
    if has_no_scheme(url):
        u_base = urlparse(base_url)
        u = urlparse(url)
        return urlunparse([u_base.scheme, u.netloc, u.path,
                           u.params, u.query, u.fragment])
    return url


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


if __name__ == '__main__':
    main()
