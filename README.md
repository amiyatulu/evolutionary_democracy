# evolutionary_democracy

Installation in ubuntu

sudo apt-get install python3-pip  
sudo pip3 install reportlab  
sudo pip3 install svglib  


Go to voting folder in terminal

python3 voting_pdf_final.py 


Generating QR code:

sudo pip3 install qrcode
qr --factory=svg "Link to all profile pdf" > profile.svg