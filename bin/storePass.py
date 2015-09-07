#!/usr/local/bin/python2.7
__author__ = 'Jason Riedel (tuxninja)'
__description__ = 'Command line utility for storing encrypted password for use with runner.'
__version__ = '1.0'

from Crypto.Cipher import AES
from Crypto import Random
import logging
import base64
import getpass
import os.path
logging.basicConfig(level=logging.INFO)

home_dir = os.path.expanduser("~")

def do_encrypt(plainText, key):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    plainText = pad(plainText)
    iv = Random.new().read(BS)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    cipherText = iv + cipher.encrypt(plainText)

    return base64.b64encode(cipherText)

def store_data(cipherText):
    pfPath = '%s/.runner/.pass' % (home_dir)
    vf = open(pfPath, 'w')
    line = "%s" % (cipherText)
    vf.write(line)
    vf.close()

    logging.info("Your password has been encrypted & stored for use with Runner.")

def get_key():
    try:
        kfPath = '%s/.runner/.key' % (home_dir)
        kf = open(kfPath)
        key = kf.readline()
        key = key.strip()
    except Exception as e:
        logging.error(e)
        exit()
    return key

if __name__ == '__main__':
    key = get_key()
    plainText = getpass.getpass("Please Enter Site Pass: ")

    cipherText = do_encrypt(plainText, key)
    store_data(cipherText)
