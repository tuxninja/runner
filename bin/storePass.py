#!/usr/bin/env python2.7
__author__ = 'jriedel'
__description__ = 'Command line utility for storing encrypted password for use with runner.'
__version__ = '1.1'

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

def create_key_file(kfPath):

    # if the directory does not exist, create it.
    kfPathDir = os.path.dirname(os.path.abspath(kfPath))
    if not os.path.exists(kfPathDir):
        os.makedirs(kfPathDir)

    print "A key file was not found, you must create one."
    key = getpass.getpass("Enter Key(16,24, or 32 characters): ")
    kf = open(kfPath, 'w')
    line = "%s" % (key)
    kf.write(line)
    kf.close()

    return key

def get_key():
    try:
        kfPath = '%s/.runner/.key' % (home_dir)
        kf = open(kfPath)
    except IOError as e:
        key = create_key_file(kfPath)
    else:
        key = kf.readline()
        key = key.strip()

    return key

if __name__ == '__main__':
    key = get_key()
    plainText = getpass.getpass("Please Enter Site Pass: ")

    cipherText = do_encrypt(plainText, key)
    store_data(cipherText)
