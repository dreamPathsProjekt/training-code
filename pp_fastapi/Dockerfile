FROM python:3.9.1

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

CMD ["hypercorn", "--bind", "0.0.0.0:8000", "cities.main:app"]