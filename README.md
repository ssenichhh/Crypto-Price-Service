# Crypto Price Service

This service provides real-time price data for cryptocurrency pairs from multiple exchanges, including Binance and Kraken. The application utilizes WebSockets to receive live price updates and makes this data available via an API built using the Django framework. The goal is to allow easy access to the latest cryptocurrency prices in a unified format, accessible through the web interface.

## Features

- Retrieves real-time cryptocurrency price data from Binance and Kraken.
- Uses WebSocket connections for both exchanges to maintain real-time data updates.
- Provides multiple API endpoints to retrieve data, including filtering options for pairs and exchanges.
- Styled web interface displaying available cryptocurrency pairs and their average prices.
- API service includes endpoints for specific pairs and exchanges.
- Deployment-ready using Docker for seamless setup and execution.

### Web Interface
- **`/`**: Displays a list of all available cryptocurrency prices from Binance and Kraken.
- **`/price/{pair}`**: Shows the latest price for a specific trading pair across exchanges. For example, `/price/ETH-BTC`.
- **`/prices/{exchange}`**: Shows all trading pairs and their respective prices for a specific exchange. For example, `/prices/binance` or `/prices/kraken`.

## Requirements
- Python 3.12
- Django 3.2
- Redis (for caching price data)
- WebSockets library (`websockets`)
- Docker and Docker Compose for deployment

## Running the Project

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/ssenichhh/Crypto-Price-Service.git
$ cd crypto_price_service
```

### Step 2: Set Up Virtual Environment
Create and activate a virtual environment:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
(venv) $ pip install -r requirements.txt
```

### Step 4: Configure Redis
Ensure Redis is installed and running locally, as it is used for caching price data. You can start Redis using Docker:
```bash
docker run -d -p 6379:6379 redis
```
### Step 5: Update Cache Settings
If you are running Redis locally without Docker, ensure your Django settings.py has the following cache configuration:
```
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
} 
```

### Step 6: Running the WebSocket Clients
Run the WebSocket clients to start receiving real-time data from Binance and Kraken:
```bash
(venv) $ python3 manage.py run_websockets
```

### Step 7: Run the Django Development Server
To start the Django server and view the web interface:
```bash
(venv) $ python3 manage.py runserver
```
Visit `http://127.0.0.1:8000/` to access the service.

## Docker Deployment

To simplify deployment, a Docker setup is provided. The Docker setup ensures all dependencies are included and configures the necessary services.

## Step 1: Update Cache Settings for Docker
If you are running the project using Docker, update the CACHES configuration in settings.py as follows:

```
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Step 2: Build and Run Docker Containers
```bash
$ docker-compose up --build
```
This will build the Docker images and run the project along with Redis.

### Step 3: Access the Service
Once the Docker containers are running, you can access the service at:
`http://127.0.0.1:8000/`

## Project Structure
```
crypto_price_project/
│
├── crypto_price_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── prices/
│   ├── management/
│   │   └── commands/
│   │       └── run_websockets.py
│   ├── templates/
│   │   └── index.html
│   ├── views.py
│   └── ...
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── ...
```

## Dockerfile
The Dockerfile is used to build the application image with all required dependencies.

```Dockerfile
# Use official Python image as a base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## docker-compose.yml
The Docker Compose configuration sets up the Django application and Redis for caching:
```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - redis
    networks:
      - app_network

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    networks:
      - app_network

networks:
  app_network:
    driver: bridge

```


