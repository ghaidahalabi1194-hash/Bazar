# Bazar.com – System Design Document

## 1. Introduction

Bazar.com is a simple online bookstore developed for the Distributed and Operating Systems course. The main idea of the project is to build a bookstore where users can search for books, view their information, and purchase available books.

We divided the system into three services: Frontend, Catalog, and Order. Each service has its own responsibility, and they communicate with each other using HTTP REST APIs and JSON.

We used Python and Flask to develop the services, SQLite to store the data, and Docker Compose to run the services in separate containers.

### 1.1 Project Objectives

The main goals of this project are:

- Allow users to search for books by topic.
- Display book information, including its price and available quantity.
- Allow users to purchase books that are in stock.
- Update the book quantity after a successful purchase.
- Store book information and order records using SQLite.
- Run the three services in separate Docker containers.
- Practice communication between services in a distributed system.




## 2. System Architecture

We divided Bazar.com into three services to make the system easier to organize and maintain. Each service handles a specific task, and all services work together to provide the bookstore functions.

### 2.1 Frontend Service

The Frontend Service is the main entry point for the client. It receives requests from the client and forwards them to the required service.

It provides three main operations:

- Search for books by topic.
- Get information about a specific book.
- Send purchase requests to the Order Service.

### 2.2 Catalog Service

The Catalog Service is responsible for managing the books. It stores the book title, topic, price, and available quantity in an SQLite database.

It provides operations to search for books, get information about a book, update its price or quantity, and reserve or release book stock.

### 2.3 Order Service

The Order Service handles book purchases. When it receives a purchase request, it checks the book information through the Catalog Service and verifies that the book is available.

If the book is in stock, the Order Service asks the Catalog Service to reserve one copy and then saves the order in its SQLite database.

If saving the order fails after reserving the book, the service tries to release the reserved copy.



## 3. Communication and APIs

The services communicate with each other using HTTP REST APIs. JSON is used to send and receive data between the services.

The client runs on the host machine and sends its requests to the Frontend Service. The Frontend then communicates with the Catalog or Order Service depending on the requested operation.

### 3.1 Available API Endpoints

The following endpoints are used in the project:

| Service | Method | Endpoint | Description |
|---|---|---|---|
| Frontend | GET | `/search/<topic>` | Search for books by topic |
| Frontend | GET | `/info/<id>` | Get information about a book |
| Frontend | POST | `/purchase/<id>` | Send a purchase request |
| Catalog | GET | `/search/<topic>` | Return matching books |
| Catalog | GET | `/info/<id>` | Return book information |
| Catalog | PUT | `/update/<id>` | Update book price or quantity |
| Catalog | POST | `/reserve/<id>` | Reserve one book copy |
| Catalog | POST | `/release/<id>` | Restore one reserved copy |
| Order | POST | `/purchase/<id>` | Process a book purchase |

### 3.2 Purchase Process

When a user wants to purchase a book, the following steps take place:

1. The client sends a purchase request to the Frontend Service.
2. The Frontend forwards the request to the Order Service.
3. The Order Service requests the book information from the Catalog Service.
4. The Order Service checks if the book is available.
5. If the book is available, the Order Service asks the Catalog Service to reserve one copy.
6. After reserving the book, the Order Service saves the order in its database.
7. The system returns a success or failure message to the client.

If the book is not available, the purchase is rejected.

## 4. Data Persistence

We used SQLite to store the data because it is simple and does not require a separate database server.

The project uses two databases:

- **Catalog Database:** Stores the books, including their IDs, titles, topics, prices, and quantities.
- **Order Database:** Stores completed orders, including the book ID, book title, price, and order date.

We also used Docker volumes to keep the database files preserved even when the containers are stopped or removed. This allows the data to remain available when the services are started again.

## 5. Docker Deployment

We used Docker to run each service in a separate Linux container. This keeps the services independent and makes it easier to run the complete system.

Docker Compose is used to build and start the three containers:

- Catalog Service runs on port `5001`.
- Order Service runs on port `5002`.
- Frontend Service runs on port `5000`.

The services communicate using their Docker Compose service names. For example, the Order Service connects to the Catalog Service using `http://catalog:5001`.

The client runs on the host machine and connects to the Frontend Service through `http://localhost:5000`.


## 6. Design Decisions, Limitations, and Future Improvements

### 6.1 Design Decisions

We divided the project into three separate services instead of building everything in one application. This makes each service responsible for a specific part of the system.

We chose Flask because it is lightweight and easy to use for building REST APIs. We also chose SQLite because the project does not need a complex database system.

Another important decision was using a separate database for the Catalog and Order services. This keeps the book information separate from the order records.

### 6.2 Limitations

The current version of Bazar.com has some limitations:

- The system does not include user accounts or login functionality.
- It does not include an online payment system.
- Book search uses an exact topic match, so it does not support advanced searching.
- The project uses a simple setup intended for the course requirements, not for a real production environment.

### 6.3 Future Improvements

In the future, the project could be improved by adding:

- User registration and login.
- An online payment feature.
- More advanced book searching and filtering.
- A better user interface for browsing books.
- More detailed order history and management.


## 7. How to Run the Project

Follow these steps to run Bazar.com:

1. Install Docker Desktop and make sure it is running.
2. Install Python on the host machine.
3. Open a terminal in the project root directory.
4. Install the client dependency:

   `pip install requests`

5. Build and start the three services using Docker Compose:

   `docker compose up --build`

6. Open another terminal in the project root directory and run the client:

   `python client/client.py`

7. Use the menu to search for books, view book information, or purchase a book.

To stop the services, run:

`docker compose down`

The Catalog and Order databases are stored in Docker volumes, so their data remains available after stopping the containers.


