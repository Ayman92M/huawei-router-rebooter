FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Set working directory
WORKDIR /app

# Copy the script
COPY reboot_router.py .

# Install Python dependencies
RUN pip install huawei-lte-api requests

# Set the command to run the script
CMD ["python", "reboot_router.py"]
