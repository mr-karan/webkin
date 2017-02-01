import logging
from os import getenv

__all__ = ['log', 'check_for_tokens']

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s -'
                    ' %(funcName)s - %(message)s')

log = logging.getLogger('webkin')


def check_for_tokens():
    log.debug('Checking for tokens')
    KINDLE_EMAIL = getenv('KINDLE_EMAIL')
    AMAZON_EMAIL = getenv('AMAZON_EMAIL')

    EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
    SMTP_HOST_NAME = getenv('SMTP_HOST_NAME')

    # DEFAULT SMTP PORT IS 587 for non SSL in GMail, SET YOURS HERE TO CHANGE

    SMTP_PORT = getenv('SMTP_PORT',587)
    MERCURY_API_KEY = getenv('MERCURY_API_KEY')
    log.debug("Tokens fetched: {} {} {} {} {} ".format(KINDLE_EMAIL, AMAZON_EMAIL,
                                                EMAIL_PASSWORD,SMTP_HOST_NAME,SMTP_PORT))

    if KINDLE_EMAIL is None or AMAZON_EMAIL is None:
        print('''
            You need to add your Kindle Verified Email Address, \n
            along with Amazon EMail ID.

            export KINDLE_EMAIL='your-kindle-email'
            export AMAZON_EMAIL='your-email-id'

            Ensure that your email address has been added to your Approved Personal Document Email List. \n
            You can check add it here : https://www.amazon.com/gp/help/customer/display.html?nodeId=201974220
        ''')
        return False

    if EMAIL_PASSWORD is None or SMTP_HOST_NAME is None:
        print('''
            You need to add your email password along with SMTP Host Name, \n

            export EMAIL_PASSWORD='your-email-password' or 'your-application-password'
            export SMTP_HOST_NAME='your-smtp-host-name-'

            NOTE: If you're using GMail and have turned on 2FA, you need to put in Application Password
            Set a new application password here : https://security.google.com/settings/security/apppasswords
        ''')
        return False

    log.debug("Mercury API Key: {}".format(MERCURY_API_KEY))
    if MERCURY_API_KEY is None:
        print('''
            Please set up a new API token for Mercury Web Parser API. \n You can do this by
            setting environment variables like so:
            export MERCURY_API_KEY='your-mercury-api-key'
            Generate the key from
            https://mercury.postlight.com/web-parser/
            ''')
        return False
    return True
