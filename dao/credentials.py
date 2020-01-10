import os

username = 'ullxgjzmgkbmwt'
password = '1e9fadb6b31275cea7047c47ca3ac93a66048caa157dde98c04d0db271bade9d'
host = 'ec2-54-195-252-243.eu-west-1.compute.amazonaws.com'
port = '5432'
database = 'd24i9iidjpn32l'
DATABASE_URI = os.getenv("DATABASE_URL",
                         'postgres://ullxgjzmgkbmwt:1e9fadb6b31275cea7047c47ca3ac93a66048caa157dde98c04d0db271bade9d@ec2-54-195-252-243.eu-west-1.compute.amazonaws.com:5432/d24i9iidjpn32l')
