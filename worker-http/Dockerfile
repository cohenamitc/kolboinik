FROM python:3

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY src/ .

CMD ["python3", "main.py"]