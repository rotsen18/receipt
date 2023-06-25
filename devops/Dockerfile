FROM python:3.11

ENV PYTHONUNBUFFERED 1
RUN mkdir /root/.ssh
COPY id_rsa /usr/src/app/
RUN mv /usr/src/app/id_rsa /root/.ssh/
RUN chmod 600 -R /root/.ssh
RUN echo "StrictHostKeyChecking no" >> /root/.ssh/config
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY devops/dpkg-req.txt /usr/src/app/
RUN apt update && apt install -y $(cat ./dpkg-req.txt)


RUN pip3 install -r requirements.txt
RUN pip install gunicorn
COPY . /usr/src/app/
WORKDIR /usr/src/app/
RUN rm -rf /root/.ssh
RUN date > .img_bilddate
CMD [ "gunicorn", "receipt.wsgi", "-c", "/usr/src/app/devops/gunicorn.conf.py"]
