import configparser

config_ = None

def config():
    global config_
    if config_ is None:
        config_ = configparser.ConfigParser()
        config_.read('config.ini')
    return config_


def main():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(YELLOW, GPIO.OUT)

    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)

    GPIO.output(GREEN, GPIO.LOW)


if __name__ == "__main__":
    # main()
    print(config().sections())
