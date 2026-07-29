FROM python:3.12-slim

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu 
    && pip install -r requirements.txt


COPY . .

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
