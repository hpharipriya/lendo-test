
# Loan-app

This project demonstrates a simplified version of a loan request-approval domain where a group of micro services handles the life cycle of a customer application. A customer application represents the intention of a customer to get a loan.
When a user sends a loan request, a customer application is created in the backend storage and send them to different bank APIs. The bank APIs will process the request and a worker program will check the status of all bank APIs asynchronously and update the Database on reaching final stages like completed or rejected.



## Tech Stack

**Programming Language:**  Python

**Framework:** Django

**Server Provider:** Nginx

**Database:** PostgreSQL

**Messaging Queue:** RabbitMQ

**Container** Docker, Docker compose




## Architecture

![architecture diagram](https://github.com/hpharipriya/lendo-BackendDeveloper-Assignment/blob/main/flow-diagram.jpg?raw=true)


## Operations

- Customer Application creation
- Send request to bank APIs
- Load message queue with the application Id
- Worker reads the queue and check the status with bank APIs
- Updates database when the status is final else IDs are loaded to message queue.

## Prerequisites 
This project assumes that Docker and docker-compose are installed.

## Project Setup and Deployment

Clone this repository 
```bash
clone repository https://github.com/hpharipriya/lendo-BackendDeveloper-Assignment.git
```

```bash
  cp .env.dist .env
```

```bash
  docker-compose build
```

```bash
  docker-compose up
```


## Environment Variables

To run this project, rename .env.dist to .env and update the secrets, if needed.



## API Reference

#### 1. Create customer application

```http
  POST http://localhost/customer/application/api/
```

| Parameter  | Type     | Description                |
| :--------  | :------- | :------------------------- |
|"first_name"| `string` | First name of customer     |                            |
| "last_name"| `string` | Last name of customer |
| "email"    | `string` | **Required**. email|
| "phone"    | `string` | **Required**. phone number |
| "dob"      | `Date`   | Date of birth |
| "address"  | `string` | address|

#### 2. Get a certain customer application

```http
  GET http://localhost/customer/application/api/<uuid>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `uuid`    | `UUIDField` | **Required**. Id of item to fetch |

#### 3. Fetch all customer application in certain status
```http
  GET http://localhost/customer/application/api/search?status=<status>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`  | `string` | **Required**. status to fetch |

