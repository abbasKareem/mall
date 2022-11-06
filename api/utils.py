from twilio.rest import Client


account_sid = "ACe892dcb54a145ef2b1f3cb2982810c5e"
auth_token = "2c04fbc3da45646a434471a8d12c1ebe"
client = Client(account_sid, auth_token)


def send_otp(mobile, otp):

    try:
        message = client.messages.create(
            to=mobile,
            from_="+447700165235",
            body=f"Your activation code is: {otp}")
        print(message.status)

    except:
        return True

    return True
