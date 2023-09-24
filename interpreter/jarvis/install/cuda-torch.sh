# This is for ubuntu 20.04 if you want to use another os or version of ubuntu go here 
# https://developer.nvidia.com/cuda-downloads?
# Also this assumes you've run the install.sh script first

# Install requirements

# Check for key and delete if it exists
if sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
then
    sudo apt-key del 7fa2af80
fi

# Download and install pin
wget /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
fi

# Checking for cuda download and downloading if not
sudo bash install/is_file.sh cuda-repo-ubuntu2004-12-2-local_12.2.2-535.104.05-1_amd64.deb https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda-repo-ubuntu2004-12-2-local_12.2.2-535.104.05-1_amd64.deb

# Unpack and install
sudo dpkg -i cuda-repo-ubuntu2004-12-2-local_12.2.2-535.104.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda

# check CUDA
if python -c "import torch; print(torch.cuda.is_available())" ; then
    nvidia -smi
else
    echo "CUDA is not available. Instillation failed"
fi
