# E-commerce Demo

This is a sample application that demonstrates an E-commerce website. The application loads 
products a Postgresql database and displays them. Users can select to display products in a single category. Users can 
click on any product to get more information including pricing, reviews and rating. Users can select items and 
add them to their shopping cart


## Getting Started
To get started  you can simply clone this `E-commerce` repository and install the dependencies.

Clone the `E-commerce` repository using git:

```bash
git clone https://github.com/mhbakhshipour/e-commerce
```

Install dependencies with this command (DEV mode):
```bash
poetry install
```

Install dependencies with this command (PROD mode):
```bash
poetry install --without dev
```

migrate models using alembic with this command:
```bash
poetry run alembic upgrade head
```

Run the application with this command:
```bash
poetry run uvicorn main:app --reload
```

## Tech Stack
* Python
* Fastapi
* Postgresql
* Redis