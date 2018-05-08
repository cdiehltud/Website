FROM python:3.5
MAINTAINER Boqi Ren <boqi.ren@tu-dresden.de>
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["start.py"]
