FROM python:3.8

ENV WORKDIRECTORY /usr/src/python-education-project
ENV TZ Europe/Kiev
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ${WORKDIRECTORY}

RUN pip3 install --upgrade pip
RUN pip3 install pipenv
COPY Pipfile Pipfile.lock ${WORKDIRECTORY}/
RUN pipenv install --system --ignore-pipfile

COPY . .

CMD ["gunicorn", "-b 0.0.0.0", "-w 2", "run:app"]
