
FROM python:latest

WORKDIR /server/

ADD requirements.txt /server/
ADD elastic_seach_mapping.json /server/
ADD app.py /server/
ADD es_client.py /server/
ADD priviledge_provider.py /server/

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]