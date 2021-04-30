import argparse
import os
import requests
import re


def make_filename(url):
    try:
        name = re.search(r'https?://(.*)', url).group(1)
    except AttributeError:
        print('URL is incorrect.')
    name = re.sub(r'\W', '-', name) + '.html'
    return name


def download(url, directory):
    r = requests.get(url)
    with open(os.path.join(directory, make_filename(url)), 'w') as f:
        f.write(r.text)


def main():
    parser = argparse.ArgumentParser(description='Download page to file')
    parser.add_argument('url')
    parser.add_argument("-o", "--output",
                        default=os.getcwd(),
                        help="Destination directory")
    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
