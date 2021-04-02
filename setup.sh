# use this file to run any setup scripts required to install the libraries
# or install the necessary libraries in general

cd AutonomousPkg
sudo ./clear.sh
python3 -m build

pkg_name=$(ls dist | grep .whl)

sudo python3 -m pip install --force-reinstall dist/$pkg_name
cd ..
