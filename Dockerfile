FROM python:3.6

ENV BARCELOCORONA /opt/barcelocorona

RUN mkdir -p $BARCELOCORONA

COPY requirements.txt $BARCELOCORONA/requirements.txt
COPY main.py $BARCELOCORONA/main.py
COPY data/ $BARCELOCORONA/data

RUN pip install -r $BARCELOCORONA/requirements.txt

WORKDIR $BARCELOCORONA
CMD ["python", "main.py"]