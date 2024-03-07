FROM python:3.11

WORKDIR /news_classifier
COPY ./app /news_classifier/app
COPY ./main.py /news_classifier/main.py
COPY ./requirements.txt /news_classifier/requirements.txt
COPY ./bst_news_classifier /news_classifier/bst_news_classifier

RUN python3 -m pip install -r requirements.txt
RUN ls -la
RUN python -m spacy download xx_ent_wiki_sm

CMD ["python3", "main.py"]