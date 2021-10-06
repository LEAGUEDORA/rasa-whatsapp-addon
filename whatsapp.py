# from flask import Flask,  request

from typing import Text, Dict
from sanic import Sanic
from sanic.response import json, HTTPResponse
from sanic.request import Request
import sms_modifier
import json



# rasa_url = "http://194.195.119.55:5005/webhooks/sellerid/webhook/"
rasa_url = "http://194.195.119.55:5005/webhooks/sellerid/webhook/"
restart_response = "Please start your conversation again."
app = Sanic("whatsapp")
file_name = "neglect_data.json"

default_error_message = "Please only select from the given category.\nPlease type '/restart' to restart the conversation"
 

class StoreTemporaryData:

    @classmethod
    def findData(cls, user: Text):
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
            return user in data
        except:
            False
    
    @classmethod
    def insertData(cls, user: Text):
        try:
            with open(file_name, "w") as f:
                data = json.load(f)
        except:
            data = []
        with open(file_name, "w") as f:
            if user in data:
                return
            data.append(user)
            json.dump(data, f)

    @classmethod
    def deleteData(cls, user: Text):
        with open(file_name, "r") as f:
            data = json.load(f)
        if user in data:
            data.remove(user)
            return


@app.route('/incoming', methods = ['POST'])
def receiveIncomingMessage(request):
    message = request.json
    user_message = message['message']
    senderID = message['sender']
    metadata = message['metadata']
    if user_message == "/restart":
        #If the user gave /restart
        try:
            sms_modifier.JSONModifier.clearData(senderID = senderID)
            sms_modifier.SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = rasa_url)
        except:
            print("No key but restarted")
        return HTTPResponse(restart_response)
    #Check_initial_user returns true for initial user or false for error or payload
    check_initial_user = sms_modifier.SMSModification.checkInitialUser(message = user_message, senderID = senderID) #Check if it the initial user or not
    if check_initial_user is True:
        # Initaial user
        user_message = user_message
    elif check_initial_user is False:
        if StoreTemporaryData().findData(senderID):
            rasa_response = sms_modifier.SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = rasa_url, metadata = metadata)
            converted_bot_response = sms_modifier.checkElements(senderID = senderID, payload = rasa_response.json()).checkAll()
            StoreTemporaryData().deleteData(senderID)
            return HTTPResponse(converted_bot_response)
        sms_modifier.JSONModifier.clearData(senderID = senderID)

        return HTTPResponse(default_error_message)
    else:
        user_message = check_initial_user
    rasa_response = sms_modifier.SendAndRecieveRasa.sendResponse(user_message = user_message, senderID = senderID, url = rasa_url, metadata = metadata)
    converted_bot_response = sms_modifier.checkElements(senderID = senderID, payload = rasa_response.json()).checkAll()
    return HTTPResponse(converted_bot_response)


if __name__ == "__main__":
    app.run(debug = True, port = 5000)