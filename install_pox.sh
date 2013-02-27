cd ~

# Build RipL:
sudo apt-get install -y python-setuptools
git clone git://github.com/brandonheller/ripl.git
cd ripl
sudo python setup.py develop

# Building Ripcord-POX
cd ~/
git clone git://github.com/brandonheller/riplpox.git
cd riplpox
#git checkout temp/hashed_fix
sudo python setup.py develop

# Building POX:
cd ~/
git clone git://github.com/noxrepo/pox.git
cd pox
git checkout master

cd ~
