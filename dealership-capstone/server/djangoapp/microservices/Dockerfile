FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/share/nltk_data

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p "$NLTK_DATA/sentiment" \
    && cp sentiment/vader_lexicon.zip "$NLTK_DATA/sentiment/vader_lexicon.zip"

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
