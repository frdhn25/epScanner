### HOW TO INSTALL & RUN ###

# Update your package linux
apt-get update && apt-get upgrade

# Git clone epScanner
git clone https://github.com/frdhn25/epScanner --depth=1

#Go to directory epScanner
cd epScanner

#Install requirements library for running the tools 
pip install -r requirements.txt

#Run the tools 
python scanner.py -u https://example.com/

or

#Run the tools for specifics path
python scanner.py -u https://expample.com/path
