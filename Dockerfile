FROM python:3.12-slim

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt

# Download Whisper model at build time (persists in the image)
ENV XDG_CACHE_HOME=/root/.cache
RUN python -c "import whisper; whisper.load_model('medium')"

COPY . .

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
