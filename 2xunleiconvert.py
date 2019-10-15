#!/usr/bin/env python
#coding:utf-8
 
import os
import base64
import sys
import re

THUNDER_HEADER = "thunder://"
THUNDER_PREFIX = "AA"
THUNDER_SUFFIX = "ZZ"
ERROR = "wrong URL"

##def is_url(func):
##    def warpper(url):
##        if re.match(r"(http|https|ftp|ed2k|thunder|qqdl)://",url):
##            return func(url)
##        else:
##            return ERROR
##    return warpper
##
##@is_url
def thunder2Real(url):
    url = url[len(THUNDER_HEADER):]
    url = url.encode("utf-8")
    url = base64.b64decode(url)
    url = url.decode("utf-8")
    url = url[len(THUNDER_PREFIX):-len(THUNDER_SUFFIX)]
    return url

if __name__ == '__main__':
    url = 'thunder://QUFodHRwOi8veDEwMi51dW5pYW8uY29tOjEwMS9kYXRhL2Jicy51dW5pYW8uY29tJUU2JTgyJUEwJUU2JTgyJUEwJUU5JUI4JTlGLyVFNyU5QiU5NyVFNiVBMiVBNiVFNyVBOSVCQSVFOSU5NyVCNC0lRTYlODIlQTAlRTYlODIlQTAlRTklQjglOUYlRTQlQjglQUQlRTYlOTYlODclRTUlQUQlOTclRTUlQjklOTUucm12Ylpa'
    print(thunder2Real(url))
