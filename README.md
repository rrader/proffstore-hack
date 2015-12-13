# proffstore-hack

curl -v https://api.github.com/repos/kpi-petitions/project-y/commits/master/statuses

$ ssh pi@139.96.30.142 "ssh -D 9050 roma@139.96.30.100"

$ curl --socks5-hostname 127.0.0.1:9050 -v https://api.github.com/repos/kpi-petitions/project-y/commits/master/statuses

rsync -a . pi@139.96.30.142:/home/pi/proffstore-hack
lsyncd -log all -nodaemon -rsyncssh . pi@139.96.30.142 /home/pi/proffstore-hack

python3 app.py


export http_proxy="http://localhost:9050"
export https_proxy="http://localhost:9050"
