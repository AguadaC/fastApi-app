FROM python:3.9-slim

ENV UNITNAME challenge

COPY . /tmp/${UNITNAME}

WORKDIR /tmp/${UNITNAME}

RUN pip install .

EXPOSE 8000

ENTRYPOINT ["challenge"]
