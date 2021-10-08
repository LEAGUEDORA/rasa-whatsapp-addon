## WhatsApp addon for Rasa

This is a code written to make this as an ADD ON to your rasa chatbot.

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

## Usage

To change RASA server URL, go to `whatsapp.py` and change

```python
RASA_URL = "http://localhost:5005/webhooks/rest/webhook/"
```

to your RASA server URL

If you wish to change the database from `JSON` to any other database you can find methods in `sms_modifier.py`. You have to change `StoreTemporaryData` and `JSONModifier` classes and update the methods.

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
