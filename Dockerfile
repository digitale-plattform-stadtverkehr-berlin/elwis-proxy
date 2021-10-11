FROM python:3-alpine

WORKDIR /usr/src/app

ENV HOST localhost
ENV PORT 8000

ENV LOG_LEVEL INFO

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY elwis_proxy.py ./

CMD [ "python", "-u", "elwis_proxy.py"]
