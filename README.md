# PyPost: Flexible Data Querying with FastAPI, Pydantic, and SQLAlchemy

PyPost is a robust and scalable backend application that implements a flexible data querying mechanism using FastAPI, Pydantic, and SQLAlchemy. It's designed with reusability and scalability in mind, ensuring easy maintenance and extension.

## Features

- Flexible and efficient data querying mechanism
- RESTful API endpoints for posts and users
- Support for filtering and including related data
- Asynchronous database operations with SQLAlchemy
- Containerized application with Docker and Docker Compose
- Database migrations with Alembic
- Comprehensive test suite

## Models

The application includes the following models:

1. Post: Belongs to a User, has many Comments and Tags
2. Comment: Belongs to a Post and a User
3. Tag: Has many Posts
4. User: Has many Comments and Posts

## API Endpoints

- `GET /api/posts?status=draft&include=tags,user`: Fetch posts filtered by status with optional inclusion of related data
- `GET /api/posts/{post_id}?include=tags,user,comments`: Retrieve a specific post by ID with optional inclusion of related data
- `GET /api/users/{user_id}?include=posts,comments`: Retrieve a specific user by ID with optional inclusion of related data

## API Documentation

Once the application is running, you can access the interactive API documentation at `http://{SERVER_HOST}:{SERVER_PORT}/docs`. This Swagger UI provides a comprehensive overview of all available endpoints, request/response schemas, and allows you to test the API directly from your browser.

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy (with asyncpg)
- Pydantic
- Alembic
- PostgreSQL
- Docker & Docker Compose
- Poetry (for dependency management)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12 (for local development)

### Running the Application

1. Clone the repository:
   ```
   git clone https://github.com/napmany/pypost.git
   cd pypost
   ```

2. Create a `.env` file in the `app` directory and configure your environment variables (use `.env.example` as a template).

3. Build and run the Docker containers:
   ```
   docker compose --env-file app/.env up --build
   ```

4. The API will be available at `http://{SERVER_HOST}:{SERVER_PORT}`.

### Running Tests

To run the test suite:
```
docker compose --env-file app/.env run --no-deps api pytest
```

### Seeding the Database

To seed the database with data:
```
docker compose --env-file app/.env run --no-deps api python src/seed.py
```

## Future Improvements

While the current implementation provides a solid foundation for flexible data querying, there are several areas where the application could be enhanced:

- Consider implementing GraphQL: If more extensive flexibility in data querying is required, GraphQL could be a powerful alternative to the current REST API. It would allow clients to request exactly the data they need in a single query, potentially improving performance and reducing over-fetching of data.

- Refine the Post status field: Currently, the `status` field in the `Post` model is implemented as a simple varchar field. It would be beneficial to discuss with the team the specific requirements for this field. Depending on the use case, it might be more appropriate to implement it as an Enum, or to add constraints to ensure only valid statuses can be set.

- Add pagination: For endpoints that could return large amounts of data, implementing pagination would improve API performance and usability.

- Enhance error handling and logging: While the current implementation includes basic error handling, a more comprehensive approach could provide better debugging capabilities and improve the overall robustness of the application.
