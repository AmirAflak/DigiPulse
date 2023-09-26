# DigiPulse
[![MIT-License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/AmirAflak/DigiPulse/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![cassandra_driver](https://img.shields.io/badge/cassandra__driver-3.28.0-blue.svg)](https://pypi.org/project/cassandra-driver/)
[![celery](https://img.shields.io/badge/celery-5.3.4-blue.svg)](https://pypi.org/project/celery/)
[![fastapi](https://img.shields.io/badge/fastapi-0.103.1-blue.svg)](https://pypi.org/project/fastapi/)
[![pydantic](https://img.shields.io/badge/pydantic-1.10.12-blue.svg)](https://pypi.org/project/pydantic/)
[![selenium](https://img.shields.io/badge/selenium-4.13.0-blue.svg)](https://pypi.org/project/selenium/)

## Description
Digipulse is a Python project designed to crawl products from the [Digikala](https://www.digikala.com) and track their prices and other characteristics. It utilizes Selenium for crawling, Redis as a queuing system for scraping tasks, CassandraDB (DataStax Cloud) for storing JSON data, and FastAPI to create a REST API for CRUD operations with the database.

The project enables you to efficiently collect and manage product data from Digikala, automating the process of tracking prices and other properties over time.

## Features
* Crawl products from the Digikala website.
* Track and monitor price changes and other characteristics of the products.
* Queue scraping tasks on Redis for efficient distribution to Celery workers.
* Store and manage JSON product data in CassandraDB on DataStax Cloud.
* Expose a REST API built with FastAPI for CRUD operations on the database.

## Installation 
1. Clone the repo
   ```sh
   git clone https://github.com/AmirAflak/DigiPulse.git
   ```
2. Navigate into the project directory:
   ```sh
   cd DigiPulse
   ```
3. Set up a Python virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install the project dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Configure the project:
* Edit config.py and adjust the necessary settings, such as database connection details and API configuration.
6. Run the application:
   ```sh
   uvicorn app.main:app --reload
   ```
   The API should now be accessible at http://localhost:8000.
  











