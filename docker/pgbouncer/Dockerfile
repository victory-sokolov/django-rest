FROM edoburu/pgbouncer:latest

COPY userlist.txt pgbouncer.ini /etc/pgbouncer/

CMD ["pgbouncer", "/etc/pgbouncer/pgbouncer.ini"]
