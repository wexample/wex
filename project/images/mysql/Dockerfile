FROM mysql:5.7.21

# Add wex conf.
COPY ./project/images/mysql/wex.cnf /etc/mysql/conf.d/
RUN chmod 644 /etc/mysql/conf.d/wex.cnf

CMD ["mysqld"]
