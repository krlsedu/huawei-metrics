FROM krlsedu/csctracker-ubuntu
RUN mkdir /my_app
ADD . /my_app
WORKDIR /my_app
RUN pip install -r requirements.txt
CMD ["python3.9","-u", "app.py"]
