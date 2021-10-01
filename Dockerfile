FROM ubuntu:20.04
USER root
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip 

WORKDIR /app
COPY / /app/
RUN pip3 install sanic
RUN pip3 install requests
CMD ["python3", "whatsapp.py"]