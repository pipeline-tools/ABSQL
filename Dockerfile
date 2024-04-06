FROM python:3.12.2-slim-bullseye
USER root

# Python Requirements
ADD dev-requirements.txt .
RUN pip3 install -r dev-requirements.txt
RUN pip3 install flake8
RUN pip3 install pytest
RUN pip3 install pytest-cov

# wd
WORKDIR /ABSQL

# Sleep forever
CMD sleep infinity
