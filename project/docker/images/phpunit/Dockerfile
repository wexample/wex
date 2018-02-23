FROM wexample/php7:latest

LABEL authors="wexample <contact@wexample.com>"

RUN wget https://phar.phpunit.de/phpunit-6.5.phar
RUN chmod +x phpunit-6.5.phar
RUN mv phpunit-6.5.phar /usr/local/bin/phpunit
