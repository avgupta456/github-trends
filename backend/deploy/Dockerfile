FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV APP_MODULE=src.main:app
ENV PORT=8000

WORKDIR /backend

COPY ../requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ../ /backend

CMD [ "/start-reload.sh" ]
