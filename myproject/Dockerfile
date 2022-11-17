FROM python:3.11-alpine
WORKDIR /
RUN apk add geos
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]