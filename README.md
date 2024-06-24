# Ticket Management System

This project is a Ticket Management System built using Python 3.11, FastAPI, Pydantic, and MongoDB. It allows for the creation of companies, boards, and tasks. It also includes a token-based login mechanism.

## Design Patterns

The application uses several design patterns:

- **Factory Pattern**: Used for creating service objects.
- **Singleton Pattern**: Ensures that a class has only one instance and provides a global point of access to it.
- **Template Pattern**: Defines the skeleton of an algorithm in a superclass, deferring some steps to subclasses.
- **Strategy Pattern**: Defines a family of algorithms, encapsulates each one, and makes them interchangeable. This will be used in the future for integrating a queue system (RabbitMQ).

## Installation

To install the necessary dependencies for this project, run the following command:

```bash
pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file:

```dotenv
TM_SECRET=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
NOSQL_URL=
NOSQL_PORT=
NOSQL_DB=
NOSQL_USER=
NOSQL_PWD=
AUTH_TOKEN_EXPIRY=
```

## Usage

To start the server, run the following command:

```bash
uvicorn main:app --reload
```

This will start the server at `http://localhost:8000`.

## Features

- **Company Management**: Create and manage companies.
- **Board Management**: Create and manage boards within companies.
- **Task Management**: Create and manage tasks within boards.
- **User Authentication**: Token-based user authentication system.

## API Endpoints

Public Endpoints:
1. `POST /public/create_user` - Endpoint to create a new user.
2. `POST /public/refresh_token` - Endpoint to refresh the user's token.
3. `POST /public/signin` - Endpoint for user sign in.
4. `POST /public/signup` - Endpoint for user sign up.

Version 1 (v1) Endpoints:
1. `GET /v1/board/{company_id}` - Endpoint to fetch a board by the company ID.
2. `GET /v1/companies` - Endpoint to fetch all companies.
3. `GET /v1/tasks/{board_id}` - Endpoint to fetch tasks by the board ID.
4. `GET /v1/user/{email}` - Endpoint to fetch a user by their email.
5. `POST /v1/create_board` - Endpoint to create a new board.
6. `POST /v1/create_company` - Endpoint to create a new company.
7. `POST /v1/create_task` - Endpoint to create a new task.
8. `POST /v1/signout` - Endpoint for user sign out.
9. `POST /v1/update_board` - Endpoint to update a board.
10. `POST /v1/update_task` - Endpoint to update a task.

SOON:
This project will be integrated with a queue system (RabbitMQ) to handle asynchronous tasks.
This system will be used for collecting logs and sending emails.
this will be done using the Strategy Pattern and can be called into controller delegates.
