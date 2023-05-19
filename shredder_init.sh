cd /local
sudo apt-get install -y libevent-dev htop
sudo chown -R $USER shredder
cd shredder
git pull && make
./shredder -c1 &
