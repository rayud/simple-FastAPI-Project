 # FastAPI Address Management API

This is a FastAPI-based RESTful API for managing addresses. It allows you to perform CRUD operations on addresses stored in a SQLite database. Additionally, it provides endpoints to list addresses with pagination and retrieve addresses within a certain distance from specified coordinates.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your_username/fastapi-address-api.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

### Create a new address

**POST** `/addresses/`

This endpoint allows you to create a new address.

### Get details of a specific address

**GET** `/addresses/{address_id}`

This endpoint fetches the details of a specified address by its ID.

### Update an existing address

**PUT** `/addresses/{address_id}`

Use this endpoint to update the details of an existing address.

### Delete an existing address

**DELETE** `/addresses/{address_id}`

This endpoint deletes an existing address from the database.

### List addresses with pagination

**GET** `/list-addresses/`

This endpoint fetches all addresses in the database with pagination enabled. You can specify the `limit` and `offset` parameters to control pagination.

### Get addresses within a distance

**GET** `/addresses/within_distance/`

This endpoint fetches the list of addresses within a certain distance from the specified coordinates. You need to provide the `latitude`, `longitude`, and `distance` parameters.

## Documentation

For detailed documentation on each endpoint and its parameters, you can access the FastAPI interactive documentation at `http://127.0.0.1:8000/docs`.

## Dependencies

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

## Authors

- [Rayudu Dola](https://github.com/rayud)

