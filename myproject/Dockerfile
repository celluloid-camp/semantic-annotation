FROM python:3.11-alpine
WORKDIR /app
EXPOSE 8000
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN apk add geos
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chmod +x ./docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]