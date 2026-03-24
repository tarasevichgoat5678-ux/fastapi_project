FROM python:3.14.3

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "nain:app", "--host","0.0.0.0","--port", "80"]