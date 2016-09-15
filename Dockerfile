from python 3.5.1



COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY . /spaceshare
WORKDIR /spaceshare
CMD ["python", "/spaceshare/server.py"]
