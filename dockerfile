# Use official Python image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port required by the assignment
EXPOSE 8000

# Start FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]