# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application files
COPY app.py /app/app.py
COPY detailer.py /app/detailer.py  
COPY imageMatcher.py /app/imageMatcher.py
COPY .env /app/.env
COPY en.wikipedia.org_detail.json /app/


# Add this line to include your custom script

# Expose the app port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
