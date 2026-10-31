# Task Manager – Cloud Computing Final Assignment

## 1. Introduction

Task Manager is a cloud-native application developed as part of a Cloud Computing course assignment.

The purpose of the project is to demonstrate how REST API microservices can be containerized using Docker, deployed using Kubernetes, and connected to a database with persistent storage.

The application consists of two independently scalable microservices, Task Service and Statistics Service, and a separate MongoDB database.

The project also demonstrates communication between microservices, Kubernetes service discovery, horizontal scaling, and database persistence.

## 2. Application Description

Task Manager allows users to create, view, update, and delete tasks through a REST API.

The application also provides statistics about the tasks, including the total number of tasks, completed tasks, and pending tasks.

The application has two main microservices:

**Task Service** is responsible for managing tasks and storing task information in MongoDB.

**Statistics Service** retrieves task information from Task Service through its REST API and calculates task statistics.

Both microservices are implemented using Python and FastAPI. They run in Docker containers and are deployed independently using Kubernetes.

## 3. Software Architecture Design

### 3.1 Architecture Overview

Task Manager uses a microservice-based architecture deployed on Kubernetes.

The system consists of three main components:

- **Task Service:** Manages tasks through a REST API.
- **Statistics Service:** Retrieves task information and calculates statistics.
- **MongoDB:** Stores task data persistently.

Each component runs in its own Docker container and is managed by a separate Kubernetes Deployment.

### 3.2 Mapping Software Components to Kubernetes Resources

| Software Component | Kubernetes Deployment | Kubernetes Service | Replicas |
|---|---|---|---|
| Task Service | `task-service` | `task-service` | 2 |
| Statistics Service | `statistics-service` | `statistics-service` | 2 |
| MongoDB | `mongodb` | `mongodb` | 1 |

Task Service and Statistics Service use LoadBalancer Services to provide access from outside the Kubernetes cluster.

MongoDB uses a ClusterIP Service and is accessible only through the cluster's internal network.

### 3.3 Communication Between Microservices

Statistics Service communicates with Task Service using HTTP and its REST API.

It sends a GET request to:

`http://task-service:8000/tasks`

Task Service connects to MongoDB using:

`mongodb://mongodb:27017/`

Kubernetes DNS allows the microservices to communicate using stable service names instead of individual Pod IP addresses.

### 3.4 Architecture Principles

The application demonstrates several cloud architecture principles:

- **Separation of responsibilities:** Each microservice has a clearly defined responsibility.
- **Loose coupling:** Statistics Service communicates with Task Service through a REST API instead of accessing its database directly.
- **Service discovery:** Kubernetes Services provide stable DNS names for communication.
- **Independent horizontal scaling:** Each REST API microservice can run multiple replicas independently.
- **Persistent storage:** MongoDB uses a PersistentVolumeClaim to preserve data when its Pod is replaced.

## 4. Benefits and Challenges of the Architecture

### 4.1 Benefits

The microservice architecture provides several technical and organizational benefits.

**Independent Scalability**

Task Service and Statistics Service can be scaled independently using Kubernetes.

For example, if the application receives many requests to create or update tasks, Task Service can be scaled without increasing the number of Statistics Service replicas.

This makes it possible to allocate computing resources according to the workload of each microservice.

**Separation of Responsibilities**

Each microservice has a clearly defined responsibility.

Task Service handles task management and database operations, while Statistics Service calculates statistics.

This separation makes the application easier to understand and allows individual services to be developed and maintained separately.

**Availability and Recovery**

Kubernetes Deployments manage the application's Pods and automatically replace Pods that fail or are deleted.

Running multiple replicas of the REST API microservices can improve availability because another replica may continue handling requests if one Pod becomes unavailable.

**Portability**

The application uses Docker containers and Kubernetes YAML configuration files.

This makes the deployment configuration reusable across compatible Kubernetes environments, although some networking and storage configuration may need to be adapted.

### 4.2 Challenges

**Increased Complexity**

A microservice architecture requires multiple Docker images, Kubernetes Deployments, Services, and configuration files.

This introduces more operational complexity compared to a monolithic application.

**Network Dependencies**

Statistics Service depends on Task Service to retrieve task information.

If Task Service becomes unavailable or responds too slowly, Statistics Service may fail to calculate statistics.

**Database Availability**

MongoDB currently runs with one replica.

Although persistent storage protects data during Pod replacement, the database remains a potential single point of failure.

**Operational Costs**

Running multiple microservices and a Kubernetes cluster requires computing resources and maintenance.

For a small application, these costs may outweigh the benefits of independent scaling.

### 4.3 Mitigation Strategies

Several mechanisms are used to reduce these challenges:

- Kubernetes Services provide stable internal network addresses.
- Kubernetes Deployments automatically replace failed Pods.
- Multiple replicas improve the availability of the REST API microservices.
- MongoDB uses a PersistentVolumeClaim to retain data when its Pod is replaced.
- Docker images provide a consistent application runtime.

Additional improvements could include monitoring, readiness and liveness probes, retry mechanisms, resource limits, database replication, and automated backups.

### 4.4 Scaling Assumptions

Task Manager is a small educational application and does not currently require multiple replicas to support its workload.

The architecture demonstrates a hypothetical business scenario in which many users create tasks and request statistics simultaneously.

In this scenario, the two microservices could experience different workloads and benefit from independent scaling.

For a small deployment with limited traffic, a monolithic application would likely be simpler and less expensive.

## 5. Security Considerations

### 5.1 Current Security Design

The application uses Kubernetes Services for communication between components.

MongoDB is exposed internally through a ClusterIP Service rather than directly through an external LoadBalancer.

Task Service and Statistics Service are exposed through LoadBalancer Services to allow browser access.

The separation between externally accessible APIs and the internal database reduces direct exposure of the database.

However, internal Kubernetes networking alone does not provide complete security.

### 5.2 Identified Security Risks

**Missing API Authentication**

The REST APIs currently do not require users to authenticate.

Anyone who can reach the API endpoints may be able to access or modify task data.

**Missing Database Authentication**

MongoDB authentication is not configured.

This means database access is not protected by database credentials within the cluster.

**Unencrypted Communication**

The application uses HTTP rather than HTTPS.

HTTP does not encrypt data transmitted between clients and API endpoints.

**Unrestricted Internal Communication**

Kubernetes NetworkPolicies have not been configured.

This means network access between Pods is not explicitly restricted by application-specific policies.

**Limited Operational Security**

The deployment has not been hardened with a complete set of container security contexts, resource limits, or automated security monitoring.

### 5.3 Proposed Security Improvements

For a production environment, the following improvements are recommended:

- Implement authentication and authorization for REST API endpoints.
- Enable MongoDB authentication.
- Store database credentials using Kubernetes Secrets.
- Configure HTTPS with TLS certificates.
- Apply Kubernetes NetworkPolicies to restrict unnecessary Pod communication.
- Use container security contexts and non-root users where possible.
- Define CPU and memory requests and limits.
- Regularly update Docker images and application dependencies.
- Implement logging, monitoring, and backup procedures.

The current implementation is intended for a local educational environment rather than public production deployment.

## 6. Business Implications

### 6.1 Cost Efficiency

Cloud computing allows organizations to allocate resources according to application demand.

Because Task Service and Statistics Service can scale independently, additional computing resources can be assigned to the service experiencing the highest workload.

This may reduce unnecessary resource usage compared to scaling the entire application.

However, Kubernetes also introduces infrastructure and operational costs.

For a small application such as Task Manager, the cost of maintaining a microservice architecture may be higher than the cost of running a simpler monolithic application.

### 6.2 Business Scalability

Independent scaling can support business growth.

For example, a task management platform used by a large organization may experience a high volume of task updates while statistics requests remain relatively low.

In that situation, Task Service could be scaled to handle increased traffic without scaling Statistics Service unnecessarily.

This provides flexibility when workload patterns change.

### 6.3 Availability and User Experience

Multiple application replicas can improve service availability.

If one Task Service Pod fails, another healthy replica may continue processing requests.

Better availability can improve user experience and reduce service interruptions.

However, the single MongoDB replica remains a limitation because database unavailability can affect the entire application.

### 6.4 Development and Maintenance

Separating application functionality into microservices can help development teams work on different components independently.

For example, one team could maintain Task Service while another team develops Statistics Service.

Individual services could also be updated without rebuilding every application component.

However, this approach increases the need for coordination, testing, deployment automation, and monitoring.

### 6.5 Business Trade-offs

The choice between microservices and a monolithic architecture depends on the size and requirements of the application.

For a small application, a monolithic architecture is often easier to develop, deploy, and maintain.

For a larger application with multiple teams and different workload patterns, microservices may provide advantages through independent scaling and separation of responsibilities.

Task Manager uses microservices primarily to demonstrate cloud computing concepts rather than because its current workload requires this level of complexity.

## 7. Kubernetes Deployment

### 7.1 Deployment Environment

The application was deployed using Kubernetes provided by Docker Desktop on Windows.

Kubernetes Deployments manage the three main components:

- Task Service
- Statistics Service
- MongoDB

The deployment configuration is stored in the project's `kubernetes` directory.

### 7.2 Container Images

The two application microservices were developed for this project and packaged into Docker images.

The images are available on Docker Hub:

- `ahmadhbg/task-service:1.1`
- `ahmadhbg/statistics-service:1.0`

MongoDB uses the official `mongo:8` container image.

### 7.3 Deployment Configuration

The tested Kubernetes deployment uses:

| Component | Replicas | Service Type |
|---|---:|---|
| Task Service | 2 | LoadBalancer |
| Statistics Service | 2 | LoadBalancer |
| MongoDB | 1 | ClusterIP |

The Kubernetes YAML files define the Deployments, Services, and persistent storage resources.

### 7.4 External Access

In the tested Docker Desktop environment, the APIs were accessible through a web browser using:

**Task Service**

`http://localhost:8000/docs`

**Statistics Service**

`http://localhost:8001/docs`

The FastAPI documentation interface allows users to inspect and test the REST endpoints.

These localhost addresses depend on the local Kubernetes environment and its LoadBalancer implementation.

### 7.5 Deployment Commands

The application can be deployed from the `kubernetes` directory using:

```powershell
kubectl apply -f .
```

The running Deployments can be inspected using:

```powershell
kubectl get deployments
```

The Kubernetes Services can be inspected using:

```powershell
kubectl get services
```

The application Pods can be inspected using:

```powershell
kubectl get pods
```

### 7.6 Independent Scaling

Both REST API microservices support horizontal scaling.

For example, Task Service can be scaled to three replicas using:

```powershell
kubectl scale deployment task-service --replicas=3
```

The deployment status can then be checked using:

```powershell
kubectl get deployments
```

Statistics Service and MongoDB do not need to change their replica counts when Task Service is scaled.

Task Service can be restored to two replicas using:

```powershell
kubectl scale deployment task-service --replicas=2
```

## 8. Database and Persistent Storage

### 8.1 MongoDB

MongoDB is used as the database for storing task information.

It runs as a separate Kubernetes Deployment with one replica.

Task Service connects to MongoDB through the internal Kubernetes Service:

`mongodb://mongodb:27017/`

### 8.2 PersistentVolumeClaim

MongoDB uses a Kubernetes PersistentVolumeClaim named `mongo-pvc`.

The PVC requests 1Gi of storage and uses the ReadWriteOnce access mode.

The persistent storage is mounted inside the MongoDB container at:

`/data/db`

This separates database storage from the lifecycle of an individual MongoDB Pod.

### 8.3 Persistence Test

A persistence test was performed during development.

The procedure was:

1. Create a task named "Learn Kubernetes" using Task Service.
2. Verify that the task exists using the `/tasks` endpoint.
3. Delete the MongoDB Pod using `kubectl delete pod -l app=mongodb`.
4. Wait for Kubernetes to create a replacement MongoDB Pod.
5. Verify that the new Pod is running.
6. Access the `/tasks` endpoint again.

**Result:** The task "Learn Kubernetes" remained available after the MongoDB Pod was replaced.

This verified persistence across MongoDB Pod replacement.

A separate test of data persistence across a complete restart of the Docker Desktop Kubernetes infrastructure has not yet been documented.

## 9. REST API Communication and Testing

### 9.1 Task Service REST API

Task Service provides REST endpoints for task management.

The API supports creating, retrieving, updating, and deleting tasks.

Task information is stored in MongoDB.

### 9.2 Statistics Service REST API

Statistics Service provides a `/statistics` endpoint.

It programmatically sends an HTTP GET request to Task Service's `/tasks` endpoint.

The returned task data is used to calculate:

- Total number of tasks
- Number of completed tasks
- Number of pending tasks

This demonstrates the ability to programmatically connect to and use a REST API.

### 9.3 Functional Testing

The following functionality was tested during development:

- Creating a task through Task Service
- Retrieving stored tasks
- Retrieving statistics through Statistics Service
- Communication between the two microservices
- Accessing the APIs through a browser
- Running multiple replicas of both microservices
- Replacing the MongoDB Pod without losing the existing task

These tests demonstrate the main functionality of the application.

## 10. Source Code and Configuration Repository

The source code, Dockerfiles, Kubernetes YAML files, architecture documentation, and deployment instructions are maintained in a GitHub repository.

**GitHub Repository:**

https://github.com/acchhe/task-manager-cloud-computing

The repository includes:

- `task_service/` – Task Service source code and Dockerfile
- `statistics-service/` – Statistics Service source code and Dockerfile
- `kubernetes/` – Kubernetes Deployments, Services, and persistent storage configuration
- `architecture/` – Architecture documentation and diagrams
- `docs/` – API documentation, demonstration plan, and final report
- `README.md` – Project overview and deployment instructions

The repository provides the configuration needed to review and reproduce the Kubernetes deployment in a compatible environment.

## 11. Demonstration

A separate demonstration plan is available in:

`docs/DEMO.md`

The planned video demonstration covers:

1. Introduction to Task Manager and its architecture
2. Kubernetes Deployments and running Pods
3. Task creation and retrieval through the REST API
4. Statistics Service and communication between microservices
5. Independent horizontal scaling
6. MongoDB persistent storage
7. Kubernetes YAML configuration and application logs
8. Security considerations and business implications

The demonstration is intended to show both the application's functionality and the underlying Kubernetes deployment.

## 12. Conclusion

Task Manager demonstrates the deployment of a microservice-based application using Docker and Kubernetes.

The application consists of two independently scalable REST API microservices and a separate MongoDB database.

It demonstrates REST API communication, Kubernetes service discovery, horizontal scaling, browser-based access, and persistent database storage.

The architecture also illustrates important trade-offs between scalability, availability, cost, security, and operational complexity.

Although Task Manager is a small educational application, the project provides practical experience with cloud-native software development and deployment.

For a production environment, further improvements would be required, particularly in authentication, encryption, monitoring, database availability, and operational security.