# install pox from repo
git clone https://github.com/noxrepo/pox.git

# install riplpox
git clone https://github.com/brandonheller/riplpox.git
cd riplpox
git checkout temp/hashed_fix
sudo python setup.py install
cd ..
