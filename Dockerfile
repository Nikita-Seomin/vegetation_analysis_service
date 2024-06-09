FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash fuw && chmod 777 /opt /run

WORKDIR /fuw

RUN mkdir /static && mkdir /data && chown -R fuw:fuw /fuw && chmod 755 /fuw

#COPY --chown=fuw:fuw djangoRestServer .

COPY . .


RUN pip install -r requirements.txt

USER fuw

CMD ["python", "manage.py", "runserver"]
