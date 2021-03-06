## WhatsApp/SMS/USSD addon for Rasa

This is a code written to make this as an ADD ON to your rasa chatbot.
This works for SMS, USSD too😁

---

## Features

- Is a sanic server
- Automatically converts the Buttons to Text and Vice-Versa
- No Database required. Users json files locally
- Easily modified individually
- Dockerized Easily / Hassle Free deployment
- Able to accept buttons and also text at a time from the users

---

## Installation

Clone this repository using

```
git clone https://github.com/LEAGUEDORA/rasa-whatsapp-addon.git
```

And then cd into the app

```sh
cd rasa-whatsapp-addon
```

Install the required packages

```
pip install -r requirements.txt
```

Run the server

```
python whatsapp.py
```

---

## Utilization

To send `text`, `image` and `buttons` you can just go do a

```python
dispatcher.utter_message(text = str, image = "", buttons = [])
```

> `sms_modifier.py` automatically converts the text, image, buttons to a single text message.

---

To restart a conversation, you have to write in `actions.py`

```python
dispatcher.utter_message(json_message = {"cmd": "restart"})
```

> This will create the data in the `users_data.json` file and works as same as rasa's restart

To neglect the user message, you have to write in `actions.py`

```python
dispatcher.utter_message(json_message = {"cmd" : "neglect"})
```

> This will check whether a payload is available and if not the same user message in **text** will be sent to rasa server. If there is a payload then the corresponding **payload** will be send to rasa server

###### Note: You are always welcomed to implement your own commands. Make sure the working of the command is written in `executeCommands` function of `checkElements` class in `sms_modifier.py` file

## Usage

To change RASA server URL, go to `whatsapp.py` and change

```python
RASA_URL = "http://localhost:5005/webhooks/rest/webhook/"
```

to your RASA server URL

If you wish to change the database from `JSON` to any other database you can find methods in `sms_modifier.py`. You have to change `StoreTemporaryData` and `JSONModifier` classes and update the methods.

###### Also do not forget to change the TODO section in `whatsapp.py` to your service provider API

---

## Deploy

This code is provided inbuilt with `Dockerfile` and `docker-compose.yml` to deploy instantly.
If **Docker** is not installed on your machine. Please follow [these steps](https://docs.docker.com/engine/install/) to install docker in your system.
You must also have to install **docker-compose** from [here](https://docs.docker.com/compose/install/) to run this on its own.

#### To run using `docker-compose`. You have to first build the image

```sh
docker build . -t whatsapp
```

> The key whatsapp can be your own image name. If know docker well, change the image name. And also don't forget to change it in the `docker-compose.yml` also.

#### To run the docker image

**Using `docker-compose`**

```
docker-compose up -d
```

## Having any doubts or want to provide suggestions?

- boyinapallisandeep@gmail.com
- 9963905554
- You are also free to create an issue in my repo😀
