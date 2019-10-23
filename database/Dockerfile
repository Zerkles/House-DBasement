FROM postgres:12.0

ENV POSTGRES_USER magda
ENV POSTGRES_PASSWORD gessler
ENV POSTGRES_DB housedb

COPY initial_scripts/ docker-entrypoint-initdb.d

EXPOSE 5432