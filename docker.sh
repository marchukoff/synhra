sudo apt-key adv --fetch-keys https://download.docker.com/linux/ubuntu/gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update -y
sudo apt install -y docker-ce
