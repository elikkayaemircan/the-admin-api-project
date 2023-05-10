FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --proxy=$http_proxy --proxy=$https_proxy --no-cache-dir --upgrade pip

RUN pip install --proxy=$http_proxy --proxy=$https_proxy --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./invs /code/invs

CMD ["uvicorn", "invs.main:app", "--host", "0.0.0.0", "--port", "8000"]
