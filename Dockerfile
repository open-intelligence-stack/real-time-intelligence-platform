FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install --no-cache-dir -r services/producer/requirements.txt \
    && pip install --no-cache-dir -r services/processor/requirements.txt \
    && pip install --no-cache-dir -r services/enricher/requirements.txt

CMD ["bash"]
