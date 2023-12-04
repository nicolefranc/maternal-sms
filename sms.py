import os
from dotenv import load_dotenv
from twilio.rest import Client



# # TODO: periodically retrieve the phone numbers and weeks postpartum from gSheets
# def dailyUpdate():
#     run()


# TODO: send SMS to patient's phone number
def sendSMS(body, to):
    load_dotenv('/.env')

    # account_sid = os.environ['ACCOUNT_SID']
    account_sid = 'ACf06fa1c0fbe207e26d94f5d61c0b3cd2'
    # auth_token = os.environ['AUTH_TOKEN']
    auth_token = '0b7c19bdff5d010c5aec4bd1e41eb1ac'
    client = Client(account_sid, auth_token)


    message = client.messages.create(
        body=body,
        to=to,
        # from_=os.environ['FROM_GAMI']
        from_='+18572541955'
    )
    return message

if __name__ == '__main__':
    body = '''HARVARD GAMI MATERNAL HEALTHCARE SMS SYSTEM

Hi Christina, this is a test message to ensure that our SMS system works with Haiti numbers. If you received this message, please respond to the email I sent.

Please do not respond to this message. Thank you.
'''

    sendSMS(body, '+50948904594')
