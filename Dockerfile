FROM python:3.13-slim

#================================================
# Migrations tool
#================================================
ADD https://github.com/amacneil/dbmate/releases/download/v2.23.0/dbmate-linux-amd64 /usr/local/bin/dbmate
RUN chmod +x /usr/local/bin/dbmate


#================================================
# PIP packages
#================================================
COPY requirements/ /tmp/requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements/dev.txt

#================================================
# Code
#================================================
RUN useradd -m -d /proj -s /bin/bash app
COPY . /proj
WORKDIR /proj
RUN chown -R app:app /proj/* && chmod +x /proj/bin/*
ENV PATH "$PATH:/proj/bin"
USER app
