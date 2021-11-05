# from flask import Flask,  request

from typing import Text, Dict
from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.request import Request
import uuid
from sms_modifier import JSONModifier, SMSModification, SendAndRecieveRasa, StoreTemporaryData, checkElements

RASA_URL = "http://localhost:5005/webhooks/rest/webhook/" #Default
RESTART_RESPONSE = "Please start your conversation again." # DEfualt
app = Sanic(str(uuid.uuid4())) #Default
DEFAULT_ERROR_MESSAGE = "Please only select from the given category.\nPlease type '/restart' to restart the conversation"
 

@app.route('/incoming', methods = ['POST'])
def receiveIncomingMessage(request):
    message = request.json

    """
    TODO: Change the below three lines according to your service provider
    """
    user_message = message['message']
    senderID = message['sender']
    metadata = message.get('metadata', None)
    if user_message == "/restart":
        #If the user gave /restart
        try:
            JSONModifier.clearData(senderID = senderID)
            SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = RASA_URL)
        except:
            print("No key but restarted")
        return HTTPResponse(RESTART_RESPONSE)
    #Check_initial_user returns true for initial user or false for error or payload
    check_initial_user = SMSModification.checkInitialUser(message = user_message, senderID = senderID) #Check if it the initial user or not
    if check_initial_user is True:
        # Initaial user
        user_message = user_message
    elif check_initial_user is False:
        if StoreTemporaryData().findData(senderID):
            rasa_response = SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = RASA_URL, metadata = metadata)
            # print(rasa_response.json())
            converted_bot_response = checkElements(senderID = senderID, payload = rasa_response.json()).checkAll()
            StoreTemporaryData().deleteData(senderID)
            return HTTPResponse(converted_bot_response)
        JSONModifier.clearData(senderID = senderID)

        return HTTPResponse(DEFAULT_ERROR_MESSAGE)
    else:
        user_message = check_initial_user
    rasa_response = SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = RASA_URL, metadata = metadata)
    # print(rasa_response.json())
    converted_bot_response = checkElements(senderID = senderID, payload = rasa_response.json()).checkAll()
    return HTTPResponse(converted_bot_response)



if __name__ == "__main__":
    app.run(debug = True, port = 5000, host = '0.0.0.0')