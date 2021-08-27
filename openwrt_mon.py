from urllib.error import HTTPError, URLError
import urllib.request
from time import sleep

url='https://heartbeat-detection-v6.thy.pub:66/'

while True:
    try:
        response = urllib.request.urlopen(url)
        response_status = response.status # 200, 301, etc
    except HTTPError as error:
        response_status = error.code # 404, 500, etc
    except URLError as error:
        response_status = error.reason # 404, 500, etc
    print(response_status, flush=True)
    sleep(1)