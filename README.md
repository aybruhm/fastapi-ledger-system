# FastAPI-Ledger

Have you ever been curious as to how fintech applications are built? This system demonstrates the basic functionalities of a fintech product.

## Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Docker and Docker-compose
- Alembic (Database migrations)
- Pytest (Unit testing)

## Problem Statement

Build a ledger system with the following functionalities: 

- [x] ( Deposit Money ) Credit X amount to one of the user’s account
- [x] ( Withdraw Money ) Debit X amount from one of the user’s account
- [x] Transfer money from one account to another account for a single user
- [x] Transfer money from one account of one user to another user
- [x] Get balance for a user
- [x] Get balance for an account of a user
- [x] User can have (10) maximum wallets

## Getting Started

To get the service up and running, follow the steps below:

1). Run the commands below in your terminal:

```bash
git clone git@github.com:aybruhm/fastapi-ledger-system.git
```

2). Change directory to fastapi-ledger-system:

```bash
cd fastapi-ledger-system
```

3). Rename the `.env.template` file to `.env` and update the values.

4). Build and run the service with:

```bash
docker-compose up --build
```

The service will build and run on port `8080`.

5). Launch a new terminal session and run the following commands:

```bash
chmod +x run-migrations.sh
```

```bash
./run-migrations.sh
```

The above commands would activate the script file and when ran- will make database migrations for you automatically.
