import socket
import socks # you need to install pysocks (see above)
import configparser

config_ = None
state_ = 'pending'
blink_status_ = False

def config():
    global config_
    if config_ is None:
        config_ = configparser.ConfigParser()
        config_.read('config.ini')
    return config_

socks.set_default_proxy(socks.SOCKS5, config()['proxy']['host'], int(config()['proxy']['port']), True)
socket.socket = socks.socksocket

import requests
from time import sleep
import threading
import RPi.GPIO as GPIO


GREEN = int(config()['GPIO']['GREEN'])
RED = int(config()['GPIO']['RED'])
YELLOW = int(config()['GPIO']['YELLOW'])


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(RED, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(YELLOW, GPIO.OUT, initial=GPIO.HIGH)


def test(session):
    r = session.get("https://api.github.com/repos/{}/{}/commits/{}/statuses".format(
            config()['remote']['user'], config()['remote']['repo'], config()['remote']['ref']
        ),
        auth=(config()['github']['username'], config()['github']['key'])
        )
    j = r.json()
    print(j)
    if j:
        return j[0]['state']


def blink_worker():
    global state_, blink_status_
    while True:
        print('Blinking {}'.format(state_))
        blink_status_ = not blink_status_
        if state_ == 'success':
            GPIO.output(GREEN, blink_status_)
            GPIO.output(YELLOW, GPIO.LOW)
            GPIO.output(RED, GPIO.LOW)
        elif state_ == 'pending':
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(YELLOW, blink_status_)
            GPIO.output(RED, GPIO.LOW)
        elif state_ == 'failure':
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(YELLOW, GPIO.LOW)
            GPIO.output(RED, blink_status_)
        if blink_status_:
            sleep(1)
        else:
            sleep(2)


if __name__ == "__main__":
    setup_gpio()

    t = threading.Thread(target=blink_worker) 
    t.start()

    s = requests.Session()
    while True:
        new_state = test(s)
        if new_state:
            state_ = new_state
        sleep(3)
