FROM python:3.11-slim

WORKDIR /backend

# Create data directory for SQLite
RUN mkdir /data && chmod 777 /data

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder into Docker
COPY ./app /backend/app

# Set Python path to recognize app module
ENV PYTHONPATH=/backend

EXPOSE 8000

# Use uvicorn with module import style
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
