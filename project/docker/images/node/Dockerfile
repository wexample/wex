FROM wexample/ubuntu17:latest

RUN apt-get update

RUN apt-get install nodejs -y

RUN apt-get install npm -y

# Install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install yarn -yqq

RUN /bin/bash
