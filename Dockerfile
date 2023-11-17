FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn playwright

# Set the working directory
WORKDIR /apps

# Expose the port the app runs on
EXPOSE 5000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

