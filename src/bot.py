from twilio_clients import client, my_phoneNumber
from message_handler import message

message = client.messages.create(
    body=message,
    from_=my_phoneNumber,
    to="whatsapp:+5511988402997",  # Implement database numbers in the future
)

print(message.body)
