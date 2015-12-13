import socket
import socks # you need to install pysocks (see above)
import configparser

config_ = None

def config():
    global config_
    if config_ is None:
        config_ = configparser.ConfigParser()
        config_.read('config.ini')
    return config_

socks.set_default_proxy(socks.SOCKS5, config()['proxy']['host'], int(config()['proxy']['port']), True)
socket.socket = socks.socksocket

import requests
from github import Github



def main():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(YELLOW, GPIO.OUT)

    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)

    GPIO.output(GREEN, GPIO.LOW)


if __name__ == "__main__":
    print(config().sections())
    s = requests.Session()
    gh = Github(config()['github']['key'])
    repo = gh.get_repo('{}/{}'.format(config()['remote']['user'], config()['remote']['repo']))
    branch = repo.get_branch(config()['remote']['ref'])
    print(branch.commit.get_statuses())
    # r = s.get("https://api.github.com/repos/kpi-petitions/project-y/commits/master/statuses")
    # print(r.text)
