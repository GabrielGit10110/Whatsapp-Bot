from twilio_clients import client, my_phoneNumber, snd_phoneNumber
from message_handler import sndMessage


def sendMessage():
    msg = client.messages.create(
        body=sndMessage,
        from_=my_phoneNumber,
        to=snd_phoneNumber,
    )
    print(msg.body)


sendMessage()
