# FastAPI-Ledger

A ledger system built with FastAPI.

## Problem Statement

Design a system called a ledger system which means there is a user and each user can have multiple accounts(at max 10 accounts). You have to design and implement following functionalities:

- [x] ( Deposit Money ) Credit X amount to one of the user’s account
- [x] ( Withdraw Money ) Debit X amount from one of the user’s account
- [x] Transfer money from one account to another account for a single user
- [x] Transfer money from one account of one user to another user
- [x] Get balance for a user
- [x] Get balance for an account of a user

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
