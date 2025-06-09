sudo ip address delete 10.242.10.101/24 dev eth1
sudo ip link set dev eth1 down
sudo ip link set dev eth2 down
sudo ip link add name bridge1 type bridge
sudo ip address add 10.242.10.101/24 dev bridge1
sudo ip link set dev bridge1 up
sudo ip link set eth2 master bridge1
sudo ip link set eth2 up
sleep 1
sudo ip link set eth1 master bridge1
sudo ip link set eth1 up
