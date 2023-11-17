# Playwright FastAPI Project

This project uses Playwright, FastAPI, and Docker to automate the process of logging into a website and retrieving system information.

## Project Structure

- `main.py`: The main FastAPI application file.
- `run_system_info_reader.py`: Contains the FastAPI router and the function to run Playwright.
- `Dockerfile`: Defines the Docker image for the application.
- `docker-compose.yaml`: Used to define and run the Docker service.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Build the Docker image and start the service:
bash docker-compose up --build


2. The application will be available at `http://localhost:5000`.

## API Endpoints

- `POST /run_system_info_reader/`: Accepts a JSON body with `username`, `password`, and `url` fields. Logs into the specified URL with the provided credentials and retrieves system information.

