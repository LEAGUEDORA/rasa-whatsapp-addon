from typing import Text, List, Dict
import json
import requests
from whatsapp import FILE_NAME_FOR_NEGLECT, FILE_NAME_FOR_USER_PAYLOAD


class StoreTemporaryData:
    """
    Stores the temporary data of the user especially the senderID that sanic needs to neglect
    """
    @classmethod
    def findData(cls, user: Text):
        try:
            with open(FILE_NAME_FOR_NEGLECT, "r") as f:
                data = json.load(f)
            return user in data
        except:
            return False
    
    @classmethod
    def insertData(cls, user: Text):
        try:
            with open(FILE_NAME_FOR_NEGLECT, "w") as f:
                data = json.load(f)
        except:
            data = []
        with open(FILE_NAME_FOR_NEGLECT, "w") as f:
            if user in data:
                return
            data.append(user)
            json.dump(data, f)

    @classmethod
    def deleteData(cls, user: Text):
        with open(FILE_NAME_FOR_NEGLECT, "r") as f:
            data = json.load(f)
        if user in data:
            data.remove(user)
            return


class SendAndRecieveRasa:
    """
    Sends the input and RASA and recieves input from RASA and sends it to the caller
    """

    @classmethod
    def sendResponse(cls, user_message: Text, senderID: Text, url: Text, metadata: Dict = {}):
        """
        Send response to RASA
        """
        payload = {
            "sender": senderID,
            "message" : user_message,
            "metadata" : metadata
        }
        try:
            response_from_rasa_server = requests.post(url, data = json.dumps(payload))
            return response_from_rasa_server
        except:
            None


class JSONModifier:

    @classmethod
    def FreshOpen(cls, file_name: str = FILE_NAME_FOR_USER_PAYLOAD):
        """
        Opening the file to store the data
        """
        with open(file_name) as users_file:
            try:
                users_data = json.load(users_file)
            except:
                users_data = {}
        return users_data

    @classmethod
    def dumpData(cls, users_data: Dict, file_name: str = FILE_NAME_FOR_USER_PAYLOAD):
        """
        Dump the userdata to the JSON File
        """
        with open(file_name, "w") as users_file:
            json.dump(users_data, users_file)
        return True
    
    @classmethod
    def clearData(cls, senderID: Text, file_name: str = FILE_NAME_FOR_USER_PAYLOAD):
        """
        Clear the data of the particular User
        """
        with open(file_name, "r+") as users_file:
            users_data = json.load(users_file)
            del users_data[senderID]
        cls.dumpData(users_data = users_data)
        return



class SMSModification:

    @classmethod
    def checkInitialUser(cls, message: Text, senderID: Text) -> bool:
        """
        Returns True if the user is initial User else return False and also the payload
        """
        users_data = JSONModifier.FreshOpen()
        try:
            users_data[senderID]
        except:
            users_data[senderID] = [message]
            JSONModifier.dumpData(users_data = users_data)
            return True
        if users_data[senderID] == []:
            users_data[senderID] = [message]
            JSONModifier.dumpData(users_data = users_data)
            return True
        try:
            payload = users_data[senderID][int(message)]
            users_data[senderID] = [message]
            JSONModifier.dumpData(users_data = users_data)
        except:
            return False
        return payload


    @classmethod
    def checkNoPayloadRequired(cls, message: Text, senderID: Text) -> bool:
        """
        If there is no Payload and Open response
        """
        users_data = JSONModifier.FreshOpen()
        if users_data[senderID] == []:
            users_data[senderID] = message
            JSONModifier.dumpData(users_data = users_data)
            return True
        return False

    @classmethod
    def InsertBotResponse(cls, senderID: Text, bot_message: List) -> Text:
        """
        Insert the bot payload 
        """
        payload_and_string = cls.readResponse(botMessage = bot_message)
        payloads = payload_and_string[0]
        string = payload_and_string[1]
        users_data = JSONModifier.FreshOpen()
        users_data[senderID] = payloads
        JSONModifier.dumpData(users_data = users_data)
        return string

    @classmethod
    def readResponse(cls, botMessage: List) -> List:
        """
        Read the bots buttons message 
        """
        buttons = botMessage[0]['buttons']
        titles = []
        payloads = []
        for i in buttons:
            payloads.append(i["payload"])
            titles.append(i["title"])
        
        return [payloads, cls.convertToString(titlesList = titles)]
    
    @classmethod
    def convertToString(cls, titlesList: List) -> Text:
        """
        Indexed Titles
        0 A
        1 B
        """
        returning_string = ""
        for index, title in enumerate(titlesList, 0):
            returning_string = returning_string + str(index) + " "  +title + "\n"
        return returning_string


    @classmethod
    def getPayload(cls, senderID: Text, userMessage: int):
        """
        Gets the exact payload
        """
        users_data = JSONModifier.FreshOpen()
        return users_data[senderID][userMessage]




class checkElements:
    """
    Checks and returns the elements contained in it
    """

    def __init__(self,senderID:Text, payload: List) -> None:
        self.senderID = senderID
        self.payload = payload
        self.text = "text"
        self.buttons = "buttons"
        self.attachment= "attachment"
        self.type= "type"
        self.payload_text = "payload"
        self.soundcloud = "soundcloud"
        self.custom = "custom"
        self.json_message = {}
    

    def checkAll(self):
        has_text = self._has_text()
        has_buttons = self._has_buttons()
        has_cmd = self._has_json_message()
        text = ""
        buttons_text = ""
        sound_text = ""
        json_message = {}
        if has_text:
            text = self.payload[0][self.text]
        if not has_buttons:
            # If returned False
            users_data = JSONModifier.FreshOpen()
            users_data[self.senderID] = []
            JSONModifier.dumpData(users_data = users_data)
        else:
            # If not false
            buttons_text = SMSModification.InsertBotResponse(self.senderID, self.payload)
        
        if has_cmd is not False:
            # If there is a command and cmd is not False
            cmd = has_cmd['cmd']
            self.executeCommands(cmd)
        return self._convertToString([text, buttons_text, sound_text])

    def _has_text(self):
        """
        Returns text if the text is available else returns False
        """
        try:
            return self.text in self.payload[0].keys()
        except:
            return False

    
    def _has_buttons(self):
        """
        Returns buttons if there are buttons else returns False
        """
        try:
            return self.buttons in self.payload[0].keys()
        except:
            return False
    
    def _has_json_message(self):
        """
        Returns the JSON message if available else returns False
        """
        try:
            return self.payload[1][self.custom]
        except:
            return False
        
    def _convertToString(self, data: List):
        """
        Converts the given buttons, text, msg list into string to form a indexed string like
        """
        return "\n".join(data)

    def executeCommands(self, command: Text):
        """
        Execudes the commands that are returned by RASA to maintain user consistency
        restart: Cleares the conversation to clear memory of the user payload
        """
        if command == 'restart':
            JSONModifier.clearData(senderID = self.senderID)
        if command == 'neglect':
            StoreTemporaryData().insertData(user = self.senderID)