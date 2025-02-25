FROM edoburu/pgbouncer:latest

COPY userlist.txt /etc/pgbouncer/
COPY pgbouncer.ini /etc/pgbouncer/

CMD ["pgbouncer", "/etc/pgbouncer/pgbouncer.ini"]
