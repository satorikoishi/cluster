cd $HOME/cloudburst
git checkout client
pip3 install -r requirements.txt
./common/scripts/install-dependencies.sh
cd $HOME/anna/client/python
sudo python3 setup.py install
cd $HOME/cloudburst
./scripts/build.sh
export PYTHONPATH=$PYTHONPATH:$(pwd)
