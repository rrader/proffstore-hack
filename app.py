import socket
import socks # you need to install pysocks (see above)
import configparser
from tts import say

config_ = None
state_ = 'pending'
blink_status_ = False

def config():
    global config_
    if config_ is None:
        config_ = configparser.ConfigParser()
        config_.read('config.ini')
        config_.read('/etc/proffstore-hack.ini')
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


def get_last_commiter(session):
    r = session.get("https://api.github.com/repos/{}/{}/commits/{}".format(
            config()['remote']['user'], config()['remote']['repo'], config()['remote']['ref']
        ),
        auth=(config()['github']['username'], config()['github']['key'])
        )
    j = r.json()
    print(j)
    if j:
        return j['commit']['committer']['name']


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
            blink_status_ = True
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(YELLOW, GPIO.LOW)
            GPIO.output(RED, blink_status_)
        if blink_status_:
            sleep(1)
        else:
            if state_ == 'success':
                sleep(15)
            else:
                sleep(2)


def trigger_change(new_state, session):
    if new_state == 'failure':
        say("Who broke the build! Ah, it's {}!".format(get_last_commiter(session)), sync=True)
        say("Bad, bad, bad developer! See what you've done! Shame on you!")
    elif new_state == 'pending':
        say("I hope it was deliberate decision to push.")
    elif new_state == 'success':
        say("Your repository looks well. For now.")


if __name__ == "__main__":
    say("Hello, my little developers.", sync=True)
    say("I am blame machine, push only good code and you will not be ashamed by the red light.", sync=True)
    setup_gpio()

    t = threading.Thread(target=blink_worker) 
    t.start()

    s = requests.Session()
    while True:
        new_state = test(s)
        if new_state:
            if new_state != state_:
                trigger_change(new_state, s)
            state_ = new_state
        sleep(3)
