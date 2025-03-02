FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
