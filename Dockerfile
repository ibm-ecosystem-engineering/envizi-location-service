FROM python:3.9-slim

WORKDIR /app

COPY ./ /app
RUN pip install -r requirements.txt

ENV LOGLEVEL INFO
ENV LOCATION_API_URL https://api.weather.com/v3/location/search
ENV LOCATION_API_KEY xxxxx
ENV OUTPUT_FOLDER  /app/output
ENV WRITE_INTERIM_FILES  FALSE
ENV FLASK_ENV production

EXPOSE 5001

CMD ["python", "-u", "main.py"]