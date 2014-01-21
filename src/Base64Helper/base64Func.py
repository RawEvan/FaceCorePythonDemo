'''
Created on 2014-1-20

@author: FaceCore
'''

# -*- coding: utf-8 -*-
#@File name    : binbase64.py
#@Auther    : GhostFromHeaven[csdn]
#@date        : 2012-07-19

from filehelper import *

#For more information about Base64 please read: http://zh.wikipedia.org/wiki/Base64

_CODE_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def binbase64(data):
    """
    Convert binary data to Base64 format string.
    """
    base64str = ""

    for i in range(len(data)/3):
        datavalue = ((data[3*i] << 16) | (data[3*i+1] << 8) | data[3*i+2])
        for j in range(4):
            base64str += _CODE_CHAR[(datavalue >> 6*(3-j)) & 0x3F]
    
    dataremain = len(data) % 3
    if dataremain == 1:
        datavalue = data[-1] << 16;
        base64str += _CODE_CHAR[(datavalue >> 18) & 0x3F]
        base64str += _CODE_CHAR[(datavalue >> 12) & 0x3F]
        base64str += "=="
    elif dataremain == 2:
        datavalue = (data[-2] << 16) | (data[-1] << 8);
        base64str += _CODE_CHAR[(datavalue >> 18) & 0x3F]
        base64str += _CODE_CHAR[(datavalue >> 12) & 0x3F]
        base64str += _CODE_CHAR[(datavalue >> 6) & 0x3F]
        base64str += "="
    return base64str

def strbase64(astr):
    """
    Convert a string to Base64 format string.
    """
    return binbase64(map(ord, astr))

class Base64Error(Exception):
    """
    Exception for Base64 error.
    """
    pass

def base64bin(encodedstr):
    """
    Convert Base64 format string to binary data.
    """
    if len(encodedstr) % 4:
        raise Base64Error("The length of input 'base64str' MUST be multiple of 4.")
    
    rawbase64str = encodedstr.rstrip("=")

    if (len(rawbase64str) % 4) == 1:
        raise Base64Error("Too many '=' characters, MUST NOT be more than 2.")

    for x in rawbase64str:
        if x not in _CODE_CHAR:
            raise Base64Error("Unexpected character %s.", x)
    
    data=[]
    for i in range(len(rawbase64str)/4):
        datavalue = (_CODE_CHAR.find(rawbase64str[4*i]) << 18) \
                    | (_CODE_CHAR.find(rawbase64str[4*i+1]) << 12) \
                    | (_CODE_CHAR.find(rawbase64str[4*i+2]) << 6) \
                    | (_CODE_CHAR.find(rawbase64str[4*i+3]))
        data.append((datavalue >> 16) & 0xFF)
        data.append((datavalue >> 8) & 0xFF)
        data.append((datavalue) & 0xFF)
    
    strremain = len(rawbase64str) % 4
    if strremain == 2:
        datavalue = (_CODE_CHAR.find(rawbase64str[-2]) << 18) \
            | (_CODE_CHAR.find(rawbase64str[-1]) << 12)
        data.append((datavalue >> 16) & 0xFF)
    elif strremain == 3:
        datavalue = (_CODE_CHAR.find(rawbase64str[-3]) << 18) \
            | (_CODE_CHAR.find(rawbase64str[-2]) << 12) \
            | (_CODE_CHAR.find(rawbase64str[-1]) << 6)
        data.append((datavalue >> 16) & 0xFF)
        data.append((datavalue >> 8) & 0xFF)

    return data

def base64str(encodedstr):
    """
    Convert Base64 format string to a string.
    """
    return "".join(map(chr,base64bin(encodedstr)))

def binfiletobase64(inp, out):
    """
    Convert binary file to Base64 format text file.
    """
    blocksize = 76 / 4 * 3
    def _binfiletobase64(fin, fout):
        while True:
            chunk = fin.read(blocksize)
            if chunk:
                fout.write(strbase64(chunk))
                fout.write("\n")
            else:
                break
    
    fileinoutpattern(inp, out, _binfiletobase64, inmode="rb", outmode="w")

def base64filetobin(inp, out):
    """
    Convert Base64 format text file to binary file.
    """
    def _base64filetobin(fin, fout):
        for line in fin:
            fout.write(base64str(line.rstrip()))
    
    fileinoutpattern(inp, out, _base64filetobin, inmode="r", outmode="wb")
