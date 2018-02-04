#!/bin/usr/env python

import requests
import itertools
from bs4 import BeautifulSoup
import os


T='''FROM microsoft/nanoserver:latest

MAINTAINER Boshi Lian <farmer1992@gmail.com>

ENV JDK_URL %s
ENV JDK_VERSION %s

''' 

STATIC=r'''
RUN powershell -NoProfile -Command \
        Invoke-WebRequest %JDK_URL% -OutFile jdk.zip; \
        Expand-Archive jdk.zip -DestinationPath '%ProgramFiles%'; \
        Move-Item '%ProgramFiles%\java*' '%ProgramFiles%\jdk'; \
        Remove-Item -Force jdk.zip

RUN setx /M JAVA_HOME "%ProgramFiles%\jdk\jre"

RUN setx /M PATH "%PATH%;%ProgramFiles%\jdk\bin"
'''

def pull_release():
    r = requests.get('http://zulu.org/download/?platform=Windows&processor=Intel x64&bitness=64')
    soup = BeautifulSoup(r.text, 'html.parser')

    for a in soup.find_all('a', class_='btn-zip'):
        url = a['href']
        filename = url.split('/')[-1]

        p = filename.split('-')

        zv = p[0].strip('zulu')
        jv = p[1].strip('jdk')

        major = jv.split('.')[0]
        minor = jv.split('.')[-1].zfill(2)

        ver = jv
        
        pjv = jv.split('.')

        if pjv[0] != '9':
            ver = '1.' + '.'.join(pjv[:-1]) + '_' + pjv[-1]

        yield major + 'u' + minor + '-' + zv, ver, url



for d,v,u in pull_release():
    try:
        os.mkdir(d)
    except:
        pass
    f = open(d + '/Dockerfile', 'w')
    with(f):
        f.write(T % (u, v))
        f.write(STATIC)

