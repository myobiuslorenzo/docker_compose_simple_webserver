#!/bin/bash
ip a | grep wl* | grep "inet [0-9\.\/]* " > inet.txt
SUBNET=$(python3 get_subnet.py)
ip route | grep default > route.txt
GATEWAY=$(python3 get_gateway.py)
echo "your subnet: $SUBNET"
echo "your gateway: $GATEWAY"
ip a | awk '/state UP/{print $2}' > physface.txt
python3 physnet.py
PFACE=$(cat physface.txt)
echo "your physical interface: $PFACE"

docker network create -d macvlan --subnet "$SUBNET" --gateway "$GATEWAY" -o parent="$PFACE" macnet
ip link set "$PFACE" promisc on

