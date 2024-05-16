FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt update && apt upgrade -y 
RUN DEBIAN_FRONTEND=noninteractive apt install tshark yara git -y
RUN git clone https://github.com/Yara-Rules/rules.git
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
