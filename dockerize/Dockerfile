# Use a standard Python 3.11 image
FROM python:3.11-buster

# Set a working directory
WORKDIR /app

# Update pip
RUN pip install --upgrade pip --no-cache-dir --use-feature=fast-deps --use-deprecated=legacy-resolver

# Install build tools and PostgreSQL client development libraries
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential

# Copy requirements and install dependencies
COPY kedegit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY kedegit/kedehub/ ./kedehub/
COPY kedegit/kedehub_client/ ./kedehub_client/

RUN mkdir -p /root/.config/KedeGit && \
    chown -R root:root /root/.config/KedeGit

# Set the entrypoint to Python with your module
ENTRYPOINT ["python", "-m", "kedehub"]

# Set default parameters which can be overridden
CMD ["--help"]
