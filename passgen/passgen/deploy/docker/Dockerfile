FROM python:3.11-alpine
LABEL maintainer="kresch"
WORKDIR /app

RUN apk update && apk upgrade && apk add --no-cache build-base gmp-dev mpfr-dev libffi-dev

COPY . .
RUN pip install poetry && poetry install && chmod +x passgen/app/bot.py

CMD ["poetry","run", "python", "passgen/app/bot.py"]

