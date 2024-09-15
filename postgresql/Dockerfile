FROM postgres:12

COPY initdb.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=challenge_db
