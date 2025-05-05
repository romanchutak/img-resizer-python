#!/usr/bin/env python
from email.headerregistry import ContentTypeHeader
import os

from flask import Flask, send_file
from flask import request
from PIL import Image
import requests
from io import BytesIO
import sys
import time
import threading
import boto3

app = Flask(__name__)


@app.route('/resizer')
def resizer():

    response = requests.get("/".join([os.environ.get('ENDPOINT_URL'), os.environ.get('BUCKET_NAME'), request.args.get('file')]))
    img = Image.open(BytesIO(response.content))
    width, height = request.args.get('width', type=int, default=100), request.args.get('height', type=int, default=100)

    width, height = width > 0 and width or 100, height > 0 and height or width
    img.thumbnail((width, height))

    print(img.size, file=sys.stdout)

    imgByteArr = BytesIO()
    img.save(imgByteArr, format=request.args.get('extension').upper(), quality=80)
    imgByteArr.seek(0)

    buff = imgByteArr.getbuffer()

    bites = buff.tobytes()

    mime = 'image/' + request.args.get('extension').lower()

    threading.Thread(target = my_task, args=[bites, request.args.get('alias'), mime,]).start()

    return send_file(imgByteArr, mimetype=mime)

def my_task(data, key, ctype):
    """Big function doing some job here I just put pandas dataframe to csv conversion"""
    time.sleep(2)
    session = boto3.session.Session()
    s3 = session.client(
        service_name = 's3',
        endpoint_url = os.environ.get('ENDPOINT_URL'),
        aws_access_key_id = os.environ.get('ACCESS_KEY'),
        aws_secret_access_key = os.environ.get('SECRET_KEY')
    )

    s3.put_object(Bucket=os.environ.get('BUCKET_NAME'), Key=key, Body=data, ContentType=ctype)

    return print('large function completed: ' + key)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)