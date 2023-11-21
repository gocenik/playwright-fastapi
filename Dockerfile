FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn playwright pytest pytest-asyncio pytest-mock aider-chat

# Set the working directory
WORKDIR /apps

# Copy your server script into the container
COPY apps/server.py .

# Expose the port the XMLRPC server runs on (adjust if your port is different)
EXPOSE 5555

# Command to run your XMLRPC server script
CMD ["python", "server.py"]
