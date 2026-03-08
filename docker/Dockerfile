FROM python:3.10

WORKDIR /app

# Copy the app folder into /app inside container
COPY ../app /app

# Install dependencies
RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]