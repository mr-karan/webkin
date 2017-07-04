#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .config import MERCURY_API_KEY
from .scaffold import *
from .send_email import send_email

from PIL import Image
from shlex import split, quote
from sys import platform as _platform, exit
from unicodedata import normalize
from logging import DEBUG

import os
import requests
import subprocess
import argparse

parser = argparse.ArgumentParser(prog='webkin')
parser.add_argument('-u', '--url', action='store', type=str,
                    help='Specify a url to parse', required=True)
parser.add_argument('-V', '--verbose', action='store_true',
                    help='Show more information on what''s happening.')
parser.add_argument('-p', '--path', metavar="path", type=str,
                    help="Path where your files will be generated")

args = parser.parse_args()

if args.verbose:
    log.setLevel(DEBUG)


def main():
    parse_url(url=args.url)


def parse_url(url):
    directory = args.path or os.path.abspath(os.path.expanduser(os.curdir))
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        log.exception('Cannot create directory: {}'.format(e))
        exit()

    log.debug('Parsing {}'.format(url))
    parse_url = 'https://mercury.postlight.com/parser?url=' + url
    data = requests.get(parse_url, headers={
                        'x-api-key': MERCURY_API_KEY}).json()
    if data is None:
        log.info("Couldn't parse the webpage.")
        exit()
    return convert_html(data, directory)


def convert_html(data, directory):
    command = ''
    try:
        title = normalize('NFKD', data['title'])
    except:
        title = 'webpage'
    filename = os.path.join(directory, title.replace(" ", "_"))
    html_file = filename + ".html"
    mobi_file = filename + ".mobi"
    img_file = filename + ".png"

    command += ' --title {} '.format(quote(title))

    if data['lead_image_url'] is not None:

        img_url = data['lead_image_url']
        try:
            im = Image.open(requests.get(img_url, stream=True).raw).resize(
                (1200, 1600),).save('{}'.format(img_file))
            command += ' --cover {} '.format(img_file)

        except:
            pass

    if data['excerpt'] is not None:
        excerpt = normalize('NFKD', data['excerpt'])
        command += ' --comments {} --output-profile kindle'.format(
            quote(excerpt))

    with open(os.path.join(directory, html_file), 'w') as template:
        clean_html = normalize('NFKD', data['content'])
        template.write(clean_html)

    if _platform == "darwin":
        try:
            build_line = ' ./ebook-convert ' + html_file + " " + mobi_file + command
            args = split(build_line)
            subprocess.call(
                args, cwd='/Applications/calibre.app/Contents/console.app/Contents/MacOS/')
        except:
            log.error('Please check if calibre CLI tools are installed.')
            exit()
    else:
        try:
            build_line = 'ebook-convert ' + html_file + " " + mobi_file + command
            args = split(build_line)
            subprocess.call(args)
        except:
            log.error('Please check if ebook-convert is added in your path.')
            exit()

    return send_email(mobi_file)


if __name__ == '__main__':
    log.info('Initiating Web-Kindle...')
    log.debug('Initiating Web-Kindle with DEBUG mode')
    if not check_for_tokens():
        exit()
    exit(main())
