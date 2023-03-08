sudo apt update
sudo apt install -y protobuf-compiler python3-pip
cd ~

# # cloudburst
# git clone https://github.com/satorikoishi/cloudburst.git
# cd cloudburst
# pip3 install -r requirements.txt
# git submodule update --init --recursive
# ./common/scripts/install-dependencies.sh
# sudo ./scripts/install-anna.sh
# ./scripts/build.sh
# cd ..

# # anna
# git clone --recurse-submodules https://github.com/satorikoishi/anna.git
# cd anna
# ./scripts/build.sh -g -j8
# cd ..

# # cluster
# git clone --recurse-submodules https://github.com/satorikoishi/cluster.git

# repos
git clone --recurse-submodules https://github.com/satorikoishi/cloudburst.git
git clone --recurse-submodules https://github.com/satorikoishi/anna.git
git clone --recurse-submodules https://github.com/satorikoishi/anna-cache.git

echo 'export HYDRO_HOME=~' >> ~/.bashrc