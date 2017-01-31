from config import MERCURY_API_KEY
from PIL import Image
from scaffold import *
from send_email import send_email
from shlex import split, quote
from sys import platform as _platform, exit
from unicodedata import normalize
from logging import DEBUG

import os
import requests
import subprocess
import argparse


parser = argparse.ArgumentParser(prog='castle')
parser.add_argument('-u', '--url', action='store', type=str,
                    help='Specify a url to parse')
parser.add_argument('-V', '--verbose', action='store_true',
                    help='Show more information on what''s happening.')
parser.add_argument('-p', '--path', metavar="path",
                    help="Path where your files will be generated")

args = parser.parse_args()


if args.verbose:
    log.setLevel(DEBUG)


def parse_url(url):
    url = args.url
    directory = args.path or os.path.abspath(os.path.expanduser(os.curdir))
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        log.exception('Cannot create directory: {}'.format(e))
        exit()

    log.debug('Parsing {}'.format(url))
    parse_url = 'https://mercury.postlight.com/parser?url=' + url
    data = requests.get(parse_url, headers={'x-api-key': MERCURY_API_KEY}).json()
    log.debug(data)
    return convert_html(data,directory)

def convert_html(data,directory):
    command = ''
    title = normalize('NFKD',data['title'])
    filename = os.path.join(directory, title.replace(" ","_"))
    html_file=filename+".html"
    mobi_file=filename+".mobi"
    img_file = filename+".png"

    command +=' --title {} '.format(quote(title))

    if data['lead_image_url'] is not None:
        img_url = data['lead_image_url']
        im = Image.open(requests.get(img_url, stream=True).raw).resize((1200,1600),).save('{}'.format(img_file))

        command += ' --cover {} '.format(img_file)

    if data['excerpt'] is not None:
        excerpt = normalize('NFKD', data['excerpt'])
        command += ' --comments {} '.format(quote(excerpt))

    with open(os.path.join(directory, html_file), 'w') as template:
        clean_html = normalize('NFKD',data['content'])
        template.write(clean_html)

    build_line=' ./ebook-convert '+html_file+" "+mobi_file+ command
    args = split(build_line)
    log.debug(args)
    if _platform == "darwin":
        try:
            subprocess.run(args, cwd='/Applications/calibre.app/Contents/console.app/Contents/MacOS/')
        except:
            log.error('Please check if calibre CLI tools are installed.')
            exit()
    else:
        try:
            subprocess.run(args, check=True, shell=True)
        except:
            log.error('Please check if ebook-convert is added in your path.')
            exit()

    return send_email(mobi_file)


if __name__=='__main__':
    log.info('Initiating castle...')
    log.debug('Initiating Castle with DEBUG mode')
    if not check_for_tokens():
        exit()
    parse_url(args.url)