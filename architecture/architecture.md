# Task Manager - System Architecture

## 1. Overview

Task Manager is a cloud-native application deployed on Kubernetes.

The application consists of two REST API microservices and a MongoDB database.

The microservices are containerized using Docker and deployed independently in Kubernetes.

## 2. System Components

### Task Service

Task Service is a REST API built with Python and FastAPI.

It manages tasks and supports creating, reading, updating, and deleting tasks.

Task data is stored in MongoDB.

### Statistics Service

Statistics Service is a REST API built with Python and FastAPI.

It communicates with Task Service over HTTP to retrieve task data.

It calculates the total number of tasks, completed tasks, and pending tasks.

### MongoDB

MongoDB is used as the application's database.

A Kubernetes PersistentVolumeClaim (PVC) provides persistent storage for database data.


## 3. Communication Between Services

The application uses Kubernetes Services for communication between components.

### Task Service and MongoDB

Task Service connects to MongoDB using the internal Kubernetes DNS name:

mongodb://mongodb:27017/

MongoDB stores the task data.

### Statistics Service and Task Service

Statistics Service communicates with Task Service using HTTP.

The internal service URL is:

http://task-service:8000

Statistics Service sends a GET request to the /tasks endpoint to retrieve task data.

It then calculates statistics based on the response.

### External Access

Both REST APIs are exposed using Kubernetes LoadBalancer Services.

Task Service is accessible at:

http://localhost:8000/docs

Statistics Service is accessible at:

http://localhost:8001/docs


## 4. Kubernetes Deployment and Scalability

The application is deployed using Kubernetes Deployments and Services.

### Deployments

Each component has its own Kubernetes Deployment:

- task-service
- statistics-service
- mongodb

Kubernetes Deployments manage the Pods running each component.

### Independent Scaling

Task Service and Statistics Service can be scaled independently.

During testing, both microservices were scaled to two replicas:

- Task Service: 2 Pods
- Statistics Service: 2 Pods
- MongoDB: 1 Pod

This demonstrates that each microservice can scale based on its own workload.

### Service Discovery and Load Balancing

Kubernetes Services provide stable network endpoints for the Pods.

When multiple replicas are running, Kubernetes Services distribute incoming requests across the available Pods.

This allows the application to handle more requests without changing the communication between microservices.


## 5. Persistent Storage

MongoDB is used to store task data.

### PersistentVolumeClaim (PVC)

The MongoDB Deployment uses a Kubernetes PersistentVolumeClaim named `mongo-pvc`.

The PVC requests 1Gi of storage and uses the ReadWriteOnce access mode.

The persistent volume is mounted inside the MongoDB container at `/data/db`.

### Data Persistence

Kubernetes Pods are temporary and can be restarted or replaced.

Without persistent storage, database data stored inside a container could be lost when the container is replaced.

The PVC allows MongoDB to retain its data when its Pod is restarted or recreated.

### Database Architecture

MongoDB runs as a separate component with one replica.

Task Service communicates with MongoDB through the internal Kubernetes Service named `mongodb`.


## 6. Persistent Storage Verification

A persistence test was performed to verify that MongoDB retains data when its Pod is replaced.

### Test Procedure

1. Created a task named "Learn Kubernetes" using Task Service.
2. Verified that the task existed in MongoDB through the `/tasks` endpoint.
3. Deleted the MongoDB Pod using the command:

   `kubectl delete pod -l app=mongodb`

4. Kubernetes automatically created a new MongoDB Pod.
5. Verified that the new MongoDB Pod was running and ready.
6. Accessed the `/tasks` endpoint again.

### Test Result

The task "Learn Kubernetes" was still available after the MongoDB Pod was replaced.

The test was successful.

This demonstrates that the MongoDB PersistentVolumeClaim preserves task data across Pod replacement.


## 7. Security Considerations

Security is an important part of deploying applications in Kubernetes.

### Internal Communication

The microservices communicate using Kubernetes Services and internal DNS names.

MongoDB uses a ClusterIP Service and is not directly exposed outside the Kubernetes cluster.

### External Access

Task Service and Statistics Service are exposed using LoadBalancer Services.

This allows users to access the REST APIs through a web browser.

### Current Security Limitations

The application currently has some security limitations:

- The REST APIs do not require authentication.
- MongoDB authentication is not configured.
- API communication uses HTTP instead of HTTPS.
- Kubernetes NetworkPolicies have not been configured.

### Possible Security Improvements

For a production environment, the following improvements are recommended:

- Add authentication and authorization to the REST APIs.
- Enable MongoDB authentication.
- Store sensitive credentials in Kubernetes Secrets.
- Use HTTPS with TLS certificates.
- Configure NetworkPolicies to restrict communication between Pods.
- Apply resource limits and security contexts to containers.