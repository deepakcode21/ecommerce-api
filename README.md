# E-Commerce Backend API

A production-ready backend built with **FastAPI** and **MongoDB**, mimicking core features of an e-commerce platform such as product listing, order placement, and order history with pagination and filtering.


## Project Structure

```
ecommerce-api/
│
├── app/                     # Main application source code
│   │
│   ├── __init__.py
│   │ 
│   ├── controllers/         # Business logic layer (between routes & DB)
│   │   ├── __init__.py
│   │   ├── order_controller.py      # Handles logic for orders (create, fetch, etc.)
│   │   └── product_controller.py    # Handles logic for products (create, filter, etc.)
│   │ 
│   ├── db/                  # Database connection and configuration
│   │   ├── __init__.py
│   │   └── database.py             # Async MongoDB connection setup using Motor
│   │ 
│   ├── models/              # Pydantic-like models used for input (API layer)
│   │   ├── __init__.py
│   │   ├── order_model.py          # Data model for Order creation
│   │   └── product_model.py        # Data model for Product creation
│   │ 
│   ├── routes/              # FastAPI route handlers (API endpoints)
│   │   ├── __init__.py
│   │   ├── order_routes.py         # Defines `/orders` endpoints and delegates to controller
│   │   └── product_routes.py       # Defines `/products` endpoints and delegates to controller
│   │ 
│   ├── schemas/             # Pydantic response/data shaping helpers
│   │   ├── __init__.py
│   │   ├── order_schema.py         # Defines how order data is returned (response schema)
│   │   └── product_schema.py       # Defines how product data is returned (response schema)
│   │ 
│   └── main.py              # Application entrypoint (creates FastAPI app and includes routers)
│
├── .env                     # Environment variables for DB URI, secret keys, etc.
├── requirements.txt         # Python dependencies list

```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/deepakcode21/ecommerce-api.git
cd ecommerce-api
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# On Windows
venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB (locally or using MongoDB Atlas)

Update the MongoDB connection string in `app/db/database.py`:

```python
MONGODB_URL= "mongodb://localhost:27017"  # or your MongoDB Atlas URI
DATABASE_NAME= "ecommerce_db"
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

### Base URL

```
http://localhost:8000
```

## API Endpoints

### 1. Create Product

**Endpoint**: `/products`
**Method**: `POST`
**Headers**:

```json
Content-Type: application/json
```

**Body:**

```json
{
  "name": "Sneakers",
  "price": 2999.99,
  "sizes": [
    { "size": "M", "quantity": 10 },
    { "size": "L", "quantity": 5 }
  ]
}
```

**Expected Response** `201 CREATED`:

```json
{
  "id": "64df5e2e78b7a2e123456789"
}
```

---

### 2. List Products

**Endpoint**: `/products`
**Method**: `GET`
**Query Parameters (optional)**:

* `name=sneak`
* `size=M`
* `limit=2`
* `offset=0`

Example URL:

```
http://localhost:8000/products
```

**Expected Response** `200 OK`:

```json
{
  "data": [
    {
      "id": "64df5e2e78b7a2e123456789",
      "name": "Sneakers",
      "price": 2999.99
    }
  ],
  "page": {
    "next": 2,
    "limit": 1,
    "previous": 0
  }
}
```

---

### 3. Create Order

**Endpoint**: `/orders`
**Method**: `POST`
**Headers**:

```json
Content-Type: application/json
```

**Body (sample):**

```json
{
  "userId": "user_1",
  "items": [
    { "productId": "64df5e2e78b7a2e123456789", "qty": 2 },
    { "productId": "64df5e2e78b7a2e999999999", "qty": 1 }
  ]
}
```

(Replace the `productId`s with actual values returned from product creation.)

**Expected Response** `201 CREATED`:

```json
{
  "id": "64df6f2e78b7a2e123456789"
}
```

---

### 4. List Orders by User

**Endpoint**: `/orders/{user_id}`
**Method**: `GET`
**Example**:

```
http://localhost:8000/orders/<userId>
```

**Expected Response** `200 OK`:

```json
{
    "data": [
        {
            "userId": "user_1",
            "items": [
                {
                    "qty": 2,
                    "productDetails": {
                        "id": "687bfd42d0629ba586ddd551",
                        "name": "Loffer"
                    }
                },
                {
                    "qty": 1,
                    "productDetails": {
                        "id": "687bfd6cd0629ba586ddd552",
                        "name": "Sneakers"
                    }
                }
            ],
            "total": 9999.97,
            "id": "687bfdadd0629ba586ddd553"
        }
    ],
    "page": {
        "next": 10,
        "limit": 1,
        "previous": 0
    }
}
```

## Testing in Postman

1. Open [Postman](https://www.postman.com/downloads/)
2. Set base URL: `http://localhost:8000`
3. Use the above APIs and example bodies to test requests.
4. For MongoDB `_id`, use returned IDs from previous POST requests.
5. Use environment variables in Postman to streamline repeated tests.

---

## Dependencies

* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [Pydantic](https://docs.pydantic.dev/)
* [Motor (Async MongoDB driver)](https://motor.readthedocs.io/)

