FROM python:3.11
ARG APP_PORT=5000

WORKDIR /service
COPY /src/ObservabilityService/* /service/
RUN pip install -r requirements.txt

EXPOSE ${APP_PORT}

CMD [ "python3", "service.py" ]