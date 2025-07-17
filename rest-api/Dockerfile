FROM python:3.9-alpine

# !!! PLESK does not work with environment variables (BUG). !!!

# Access to /shared/ volume.
# ENV OPENDATA_AUDIT_OUTPUT=/shared/audit.json

# Copy Filesystem.
WORKDIR /app/rest-api
COPY . .

# Install Requirements.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the API.
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

