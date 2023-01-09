FROM python:3.10

RUN mkdir /mangaread

WORKDIR /mangaread/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /mangaread

CMD ["python", "manage.py runserver"]
