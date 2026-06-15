FROM debian:bookworm

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends gnupg2 wget \
    && wget -O - https://apt.wexample.com/gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/wexample.gpg \
    && echo "deb http://apt.wexample.com/ stable main" > /etc/apt/sources.list.d/wexample.list \
    && apt-get update -qq \
    && apt-get install -y wex \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
