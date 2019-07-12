import json
import smtplib


class Emailer:
    def __init__(self):
        with open("email.json", "r") as email_json:
            self.email_json = json.loads(email_json.read())
            self.from_address = self.email_json['email_address']
            self.emailing = smtplib.SMTP(host=self.email_json['host'])
            self.emailing.ehlo()
            self.emailing.starttls()
            self.emailing.login(user=self.email_json['email_address'],
                                password=self.email_json['password'])

    def send_email(self, email_address, event_key):
        msg = smtplib.email.message_from_string(f'Hello! \nYour ReMatch run for {event_key} has completed. To download '
                                                f'the match clips, visit ftp://tweirtx.me and download the ZIP file '
                                                f'named "{event_key}.zip". When you unzip it, the match clips ' \
                                                'will be inside, named as match_key.mp4. \n\nPlease email me back once '
                                                'you have downloaded the videos, and please let me know if you have any'
                                                ' issues or questions. \n\nThanks for using ReMatch! \n\nTravis Weir')
        msg['subject'] = "Your ReMatch download is ready!"
        msg['From'] = "ReMatch <{}>".format(self.from_address)
        self.emailing.send_message(msg=msg, to_addrs=[email_address])
