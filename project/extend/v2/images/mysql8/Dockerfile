FROM mysql:8.0.22

# Add wex conf.
COPY ./v2/images/mysql/wex.cnf /etc/mysql/conf.d/
RUN chmod 644 /etc/mysql/conf.d/wex.cnf

CMD ["mysqld"]
