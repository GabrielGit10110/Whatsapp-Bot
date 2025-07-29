from flask import Flask, request, Response
from twilio_clients import client, my_phoneNumber, snd_phoneNumber
from twilio.twiml.messaging_response import MessagingResponse
from message_handler import mainMenu, deliveryMenu
from message_handler import sizeMenu, colorMenu, Bicicleta


# Instantiate the Flask Class
app = Flask(__name__)


# Initial Message
def sendInitialMessage():
    msg = client.messages.create(
        body=mainMenu,
        from_=my_phoneNumber,
        to=snd_phoneNumber,
    )

    # Debug
    print(f"Sending Message to {snd_phoneNumber}, from {my_phoneNumber}")
    print(msg.body)


# Current user state (selecting the color, selecting the size, etc)
user_state = {}


@app.route("/reply_wpp", methods=['POST'])
def handleMsg():
    sender = request.form.get('From')  # The phone number of the client
    incomingMsg = request.form.get('Body', '').strip().lower()

    # Boot the user if it's not yet booted
    if sender not in user_state:
        user_state[sender] = {'bike': Bicicleta("", "", ""), 'in_menu': True}

    bike = user_state[sender]['bike']
    resp = MessagingResponse()

    # Bot logic, get the state of the user and calls the appropriate functions
    if user_state[sender].get('selecting_color'):
        bike = selectColor(bike, incomingMsg)
        user_state[sender]['selecting_color'] = False
        resp.message(f"Cor {bike.color} selecionada!\n{mainMenu}")
    elif user_state[sender].get('selecting_size'):
        bike = selectSize(bike, incomingMsg)
        user_state[sender]['selecting_size'] = False
        resp.message(f"Tamanho {bike.size} selecionado!\n{mainMenu}")
    elif user_state[sender].get('selecting_delivery'):
        bike = selectDelivery(bike, incomingMsg)
        user_state[sender]['selecting_delivery'] = False
        resp.message(f"Entrega por {bike.delivery} selecionada!\n{mainMenu}")
    else:
        match incomingMsg:
            case "1":
                user_state[sender]['selecting_color'] = True
                resp.message(colorMenu)
            case "2":
                user_state[sender]['selecting_size'] = True
                resp.message(sizeMenu)
            case "3":
                user_state[sender]['selecting_delivery'] = True
                resp.message(deliveryMenu)
            case "4":
                resp.message(f"Resumo:\nCor: {bike.color}\nTamanho: {
                             bike.size}\nEntrega: {bike.delivery}\n10 - Voltar")
            case "9":
                user_state[sender] = {'bike': Bicicleta(
                    "", "", ""), 'in_menu': True}
                resp.message(
                    f"Conversa resetada. Digite uma opção: \n{mainMenu}")
            case "10":
                resp.message(
                    f"Voltando ao inicio...\n{mainMenu}"
                )
            case _:
                resp.message("Opção inválida. " + mainMenu)

    return str(resp)


# Takes the user to the different menus, and define the attributes of the
# shopping order
def selectColor(bike, incomingMsg):
    match incomingMsg:
        case "1" | "azul":
            bike.color = "Azul"
        case "2" | "vermelho":
            bike.color = "Vermelho"
        case "3" | "amarelo":
            bike.color = "Amarelo"
        case "4" | "verde":
            bike.color = "Verde"
        case "10" | "voltar":
            bike.color = ""
    return bike


def selectSize(bike, incomingMsg):
    match incomingMsg:
        case "1" | "pequeno":
            bike.size = "Pequeno"
        case "2" | "medio":
            bike.size = "Medio"
        case "3" | "grande":
            bike.size = "Grande"
        case "10" | "voltar":
            bike.size = ""
    return bike


def selectDelivery(bike, incomingMsg):
    match incomingMsg:
        case "1" | "carro":
            bike.delivery = "Carro"
        case "2" | "aviao":
            bike.delivery = "Avião"
        case "3" | "navio":
            bike.delivery = "Navio"
        case "10" | "voltar":
            bike.delivery = ""
    return bike


def runApp():
    app.run(port=3000)
