sudo ip addr add 139.96.30.100/24 dev enp3s0
sudo systemctl start dhcpd4@enp3s0
sudo systemctl start sshd
sudo systemctl start dnsmasq
sudo systemctl stop dropbox
sudo killall dropbox

#==============

while ! ping -c 1 139.96.30.142 -W 1; do
sleep 1;
done

#==============

ssh pi@139.96.30.142 'sudo su -c "echo nameserver 139.96.30.100 > /etc/resolv.conf"'
ssh pi@139.96.30.142 'amixer sset PCM 120'
#======================
exit 0
# IN SEPARATE TERMINALS:
ssh pi@139.96.30.142 "ssh -D 9050 roma@139.96.30.100"
ssh pi@139.96.30.142 'sudo su -c "cd /home/pi/proffstore-hack; /home/pi/venv/bin/python app.py"'
