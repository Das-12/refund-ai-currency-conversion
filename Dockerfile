# Use a base image that has Python and required build tools
FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Create a supervisor config directory
RUN mkdir -p /etc/supervisor/conf.d

# Copy the supervisor configuration file
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Command to run supervisor which will manage the processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]

# Use a base image that has Python and required build tools
# FROM python:3.12

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     pkg-config \
#     default-libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory
# WORKDIR /app

# # Copy requirements.txt first to leverage Docker cache
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your application (update as needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
