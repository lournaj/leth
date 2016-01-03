FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD ./src/requirements.txt /app/
ADD ./src/requirements_dev.txt /app/
RUN pip install -r requirements_dev.txt
ADD ./src/gunicorn.py /app/
ADD ./src /app
CMD ["gunicorn", "--config=gunicorn.py", "leth.wsgi:application"]
