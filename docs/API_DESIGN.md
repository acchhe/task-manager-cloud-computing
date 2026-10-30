# Task Manager – REST API Design

## 1. Overview

Purpose:
The purpose of the Task Manager Application is to create an application that can store, organize and calculate statistics for created tasks by end users.

Architecture:
The application consists of two microservices: The Task Service that manages tasks and communicates with the MongoDB, and the Statistics Service which retrieves tasks and calculates statistics by calling the Task Service.

Communication:
Communication between Service-components is done through HTTP requests using REST APIs. The Task Service communicates with MongoDB through a database driver rather than a REST API.

## 2. Task Service API

The main responsibility of the Task Service is to manage tasks created by end users. It provides REST API endpoints for creating, retrieving, updating, and deleting tasks stored in MongoDB.

GET /tasks

The GET /tasks endpoint allows clients to retrieve all stored tasks. The Task Service queries MongoDB and returns the retrieved tasks as a JSON response.

POST /tasks

The POST /tasks endpoint allows clients to create a new task. The Task Service receives task information in JSON format, validates the input, and stores the new task in MongoDB.

GET /tasks/{id}

The GET /tasks/{id} endpoint allows clients to retrieve a specific task using its unique identifier. The Task Service queries MongoDB and returns the corresponding task as a JSON response.

PUT /tasks/{id}

The PUT /tasks/{id} endpoint allows clients to update an existing task identified by its unique ID. The Task Service validates the provided JSON data and updates the corresponding task in MongoDB.

DELETE /tasks/{id}

The DELETE /tasks/{id} endpoint allows clients to delete a specific task using its unique identifier. The Task Service locates and removes the corresponding task from MongoDB.


## 3. Statistics Service API

Responsibility:
The main responsibility of the Statistics Service is to calculate statistics on stored and existing tasks. The Statistics Service retrieves the task data by sending HTTP requests to the Task Service through its REST API. The Task Service, in turn, retrieves the requested information from MongoDB.

GET /statistics

The GET /statistics endpoint allows clients to retrieve statistical calculations on tasks stored in MongoDB. The Statistics Service retrieves task data from the Task Service and returns information such as the total number of tasks, completed tasks, and pending tasks in JSON format.



## 4. Data Models

Each task consists of four attributes: id, title, description, and completed.

The id attribute uniquely identifies each task and allows individual tasks to be retrieved, updated, or deleted. MongoDB automatically generates a unique _id value when a new task is created. This identifier is represented as a string in the REST API.

id: Unique identifier generated automatically
Datatype: String

title: Title of the task
Datatype: String

description: Description of the task
Datatype: String

completed: Tells whether or not the task is completed
Datatype: Boolean

## 5. Service Communication

The Task Manager application uses REST APIs over HTTP to enable communication between its microservices.

When a client requests task statistics through the GET /statistics endpoint, the Statistics Service sends an HTTP GET request to the Task Service using its GET /tasks endpoint. The Task Service retrieves the stored tasks from MongoDB and returns the data to the Statistics Service as a JSON response.

The Statistics Service processes the retrieved data to calculate the total number of tasks, completed tasks, and pending tasks. The calculated statistics are then returned to the client in JSON format.

Communication between the Task Service and MongoDB is handled through the PyMongo database driver using the MongoDB protocol, rather than REST.

This architecture separates responsibilities between the microservices and allows them to be developed, deployed, and scaled independently.

## 6. Error Handling

The Task Manager application will implement error handling to ensure that invalid requests and unexpected failures are handled appropriately without causing the microservices to crash.

Both the Task Service and Statistics Service will use standard HTTP status codes to communicate the outcome of API requests. Successful requests will return appropriate status codes, while unsuccessful requests will return meaningful error messages in JSON format.

The following HTTP status codes are planned for the application:

HTTP Status Code

Description

200 OK

The request was successfully processed.

201 Created

A new task was successfully created.

204 No Content

A task was successfully deleted.

400 Bad Request

The request contains invalid information, such as an incorrectly formatted task ID.

404 Not Found

The requested task does not exist.

422 Unprocessable Content

The submitted data does not meet the API's validation requirements.

500 Internal Server Error

An unexpected internal error occurred.

503 Service Unavailable

A required service or database is temporarily unavailable.

The Task Service will validate incoming data before performing database operations. If a requested task cannot be found, the service will return a 404 Not Found response.

If MongoDB becomes unavailable, the Task Service will handle the database connection failure and return an appropriate error response. Similarly, if the Statistics Service cannot communicate with the Task Service, it will return a service availability error rather than an incorrect statistical result.

Error responses will provide useful information to clients without exposing sensitive system details, such as database credentials or internal configuration.