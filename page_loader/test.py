from bs4 import BeautifulSoup
import requests
import re
import os


def make_filename(url, type='html'):
    name = re.search(r'https?://(.*)', url).group(1)
    if type == 'html':
        name = re.sub(r'\W', '-', name) + '.html'
    elif type == 'dir':
        name = re.sub(r'\W', '-', name) + '_files'
    elif type == 'resource':
        print(f'URL is {url}, type is {type}')
        name = re.sub(r'\W', '-', name)
    return name


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


url = 'https://linkmeup.ru/blog/473.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
for img in soup.find_all('img'):
    link = img.get('src')
    print(link)
    if is_relative_link(link):
        link = absolute_link(link, get_domain(url))
    if is_subdomain(url, link):
        image_file_path = os.path.join(directory,
                                       make_filename(url, type='dir'),
                                       make_filename(link, type='resource'))
        print(image_file_path)
        with open(image_file_path, 'w') as image_file:
            image_file.write(requests.get(link))
    # print(img.text)
    # break
