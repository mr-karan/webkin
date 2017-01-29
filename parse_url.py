from unicodedata import normalize

import os
import requests
import subprocess
from shlex import split, quote
import logging
import argparse

from sys import exit
from scaffold import *

from config import MERCURY_API_KEY
from send_email import send_email

parser = argparse.ArgumentParser(prog='castle')
parser.add_argument('-u', '--url', action='store',
                    help='Specify a url to parse', default=True)
parser.add_argument('-V', '--verbose', action='store_true',
                    help='Show more information on what''s happening.')
parser.add_argument('-o', '--output', type=str, action='store',
                    nargs='*', help='Specify download directory.')

args = parser.parse_args()

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s -'
                    ' %(funcName)s - %(message)s')

log = logging.getLogger('castle')

if args.verbose:
    log.setLevel(logging.DEBUG)


def parse_url(url):
    url = args.url
    parse_url = 'https://mercury.postlight.com/parser?url=' + url
    r = requests.get(parse_url, headers={'x-api-key': MERCURY_API_KEY}).json()
    return convert_html(r)

def convert_html(data):
    command = ''

    title = normalize('NFKD',data['title'])
    command +=' --title {} '.format(quote(title))
    if data['lead_image_url'] is not None:
        command += ' --cover {} '.format(data['lead_image_url'])
    if data['excerpt'] is not None:
        excerpt = normalize('NFKD', data['excerpt'])
        command += ' --comments {} '.format(quote(excerpt))

    filename = title.replace(" ","_")
    html_file=os.getcwd()+"/"+filename+".html"
    mobi_file=os.getcwd()+"/"+filename+".mobi"

    with open(html_file, 'w') as the_file:
        clean_html = normalize('NFKD',data['content'])
        the_file.write(clean_html)

    build_line=' ./ebook-convert '+html_file+" "+mobi_file+ command
    args = split(build_line)
    print(args)
    try:
        subprocess.run(args,cwd='/Applications/calibre.app/Contents/console.app/Contents/MacOS/')
    except:
        return "Couldn't convert"
    return send_email(mobi_file)


if __name__=='__main__':
    log.info('Initiating castle...')
    log.debug('Initiating Castle with DEBUG mode')
    if not check_for_tokens():
        exit()
    parse_url()