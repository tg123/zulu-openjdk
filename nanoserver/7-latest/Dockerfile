FROM microsoft/nanoserver:latest

MAINTAINER Boshi Lian <farmer1992@gmail.com>

ENV JDK_URL https://cdn.azul.com/zulu/bin/zulu7.22.0.3-jdk7.0.171-win_x64.zip
ENV JDK_VERSION 1.7.0_171

RUN powershell -NoProfile -Command \
        Invoke-WebRequest %JDK_URL% -OutFile jdk.zip;

RUN powershell -NoProfile -Command \
        Expand-Archive jdk.zip -DestinationPath '%ProgramFiles%'; \
        Move-Item '%ProgramFiles%\zulu*' '%ProgramFiles%\zulujdk'; \
        Remove-Item -Force jdk.zip

RUN setx /M JAVA_HOME "%ProgramFiles%\zulujdk\jre"

RUN setx /M PATH "%PATH%;%ProgramFiles%\zulujdk\bin"
