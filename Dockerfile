FROM ubuntu:20.04
USER root
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip 
WORKDIR /app
COPY / /app/
RUN pip3 install -r requirements.txt
RUN chmod 777 users_data.json
RUN chmod 777 neglect_data.json
CMD ["python3", "whatsapp.py"]