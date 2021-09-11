FROM ubuntu:20.04
USER root
ENTRYPOINT []
WORKDIR /app
COPY / /app/
RUN pip3 install flask
CMD ["python3", "whatsapp.py"]