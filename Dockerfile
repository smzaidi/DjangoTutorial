#A python-3.7.x application; currently, I am running v 3.7.2
FROM python:latest
MAINTAINER smzaidi "smzaidi@umich.edu"
ENV PYTHONUNBUFFERED=1
RUN apt-get update -y
WORKDIR /app
COPY . .
RUN chmod g+rw -R .

RUN pip install -r requirements.txt
# RUN adduser -D user
# USER user

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
