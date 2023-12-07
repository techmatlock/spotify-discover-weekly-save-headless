FROM python:3.11.7-slim

ENTRYPOINT ["tail", "-f", "/dev/null"]

WORKDIR .

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

