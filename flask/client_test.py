import requests
import time

# disable useless message
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IP = '0.0.0.0'
PORT = '8080'
URL_BASE = 'http://{}:{}'.format(IP, PORT)

def print_response(response):
    print()
    print('================')
    print('request: {}'.format(response.request))
    print('url: {}'.format(response.url))
    print('status code: {}'.format(response.status_code))
    print()
    print(response.text)
    print('================')
    print()


def test_html():
    response = requests.get(URL_BASE + '/')
    print_response(response)
    time.sleep(0.5)

    response = requests.get(URL_BASE + '/test')
    print_response(response)
    time.sleep(0.5)


def test_restapi():
    # GET
    response = requests.get(URL_BASE + '/api/v1/test')
    print_response(response)
    time.sleep(0.5)

    response = requests.get(URL_BASE + '/api/v1/test2')
    print_response(response)
    time.sleep(0.5)

    # POST
    body = {'test':'test'}
    response = requests.post(URL_BASE + '/api/v1/test', json=body)
    print_response(response)
    time.sleep(0.5)

    response = requests.post(URL_BASE + '/api/v1/test2', json=body)
    print_response(response)
    time.sleep(0.5)

    # PUT
    response = requests.put(URL_BASE + '/api/v1/test', json=body)
    print_response(response)
    time.sleep(0.5)

    response = requests.put(URL_BASE + '/api/v1/test2', json=body)
    print_response(response)
    time.sleep(0.5)

    # DELETE
    response = requests.delete(URL_BASE + '/api/v1/test')
    print_response(response)
    time.sleep(0.5)

    response = requests.delete(URL_BASE + '/api/v1/test2')
    print_response(response)
    time.sleep(0.5)

if __name__ == '__main__':
    test_html()
