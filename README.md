# E-commerce Demo

This is a sample application that demonstrates an E-commerce website. The application loads 
products a Postgresql database and displays them. Users can select to display products in a single category. Users can 
click on any product to get more information including pricing, reviews and rating. Users can select items and 
add them to their shopping cart

Here are screenshots that show the E-commerce application in use.

**Home Page**
![Home Page]()

---

**Item Detail Page**
![Item Detail]()

---

**Shopping Cart**
![Shopping Cart]()

## Getting Started
To get started  you can simply clone this `E-commerce` repository and install the dependencies.

Clone the `E-commerce` repository using git:

```bash
git clone https://github.com/mhbakhshipour/e-commerce
```

Install dependencies with this command:
```bash
poetry install
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