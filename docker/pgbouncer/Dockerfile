FROM edoburu/pgbouncer:v1.24.1-p1

COPY userlist.txt pgbouncer.ini /etc/pgbouncer/

CMD ["pgbouncer", "/etc/pgbouncer/pgbouncer.ini"]
