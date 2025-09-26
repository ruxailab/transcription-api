FROM wallies/python-cuda:3.12-cuda12.2-runtime

# install ffmpeg
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

# Set the working directory to /sentiment-analysis-api
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .


# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code
COPY . .

# Expose port used by uvicorn (Make port 8000 available to the world outside this container)
EXPOSE 8000


# Run the application
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
