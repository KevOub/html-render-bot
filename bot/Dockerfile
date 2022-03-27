FROM python:3.10-bullseye
RUN mkdir /app
ADD . /app
WORKDIR /app
# RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt 
CMD ["python", "bot.py"]