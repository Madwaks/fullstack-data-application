FROM python:3.13.1-slim-bookworm

WORKDIR /app

COPY . .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0", "--port=5001" ]
