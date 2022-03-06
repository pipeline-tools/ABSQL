FROM python:3.9.1-slim-buster
USER root

# Python Requirements
ADD requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install flake8
RUN pip3 install pytest
RUN pip3 install pytest-cov

# wd
WORKDIR /ABSQL

# Sleep forever
CMD sleep infinity
