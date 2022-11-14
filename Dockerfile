FROM python:3.8-buster
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

RUN pip install -r requirements.txt
