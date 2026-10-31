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



## 8. Architecture Benefits and Challenges

### Benefits

The microservice architecture provides several benefits:

- Independent scaling: Task Service and Statistics Service can be scaled separately based on demand.
- Separation of responsibilities: Each microservice has a specific purpose.
- Independent deployment: Individual services can be updated without rebuilding the entire application.
- Portability: Docker containers and Kubernetes configuration make deployment more consistent across environments.

### Challenges

The architecture also introduces challenges:

- Increased complexity: Multiple services require more configuration and monitoring.
- Network communication: Statistics Service depends on HTTP communication with Task Service.
- Service availability: If Task Service becomes unavailable, Statistics Service cannot retrieve current task data.
- Operational overhead: Kubernetes requires additional resources and knowledge compared to running a single application.

### Mitigation Strategies

The application uses Kubernetes Services for stable service discovery and Deployments for automatic Pod replacement.

Multiple replicas improve the availability of the REST API microservices.

Further improvements could include health checks, monitoring, retries, resource limits, and stronger security controls.

### Application Size and Scaling

Task Manager is a small educational application and does not currently require multiple replicas to handle its workload.

The scaling demonstration represents a hypothetical scenario where many users create tasks and request statistics simultaneously.

In such a scenario, independent scaling could help handle increased traffic.


## 9. Business Implications

### Cost Efficiency

Cloud computing allows organizations to adjust computing resources based on demand.

Task Service and Statistics Service can be scaled independently, which may reduce unnecessary resource usage compared to scaling the entire application.

However, running multiple microservices and Kubernetes also introduces infrastructure and maintenance costs.

### Scalability and Business Growth

If the number of users increases, the application can scale its microservices independently.

For example, a company may experience a high number of task updates while statistics requests remain relatively low.

In this scenario, Task Service can be scaled without increasing the number of Statistics Service replicas.

### Availability and Reliability

Multiple replicas can improve service availability.

If one application Pod fails, Kubernetes can replace it, while other healthy replicas may continue handling requests.

However, MongoDB currently runs as a single replica and remains a potential single point of failure.

### Maintenance and Development

Separating functionality into microservices can make it easier for development teams to maintain and update individual components.

However, this approach also increases operational complexity because multiple services must be deployed, monitored, and secured.

### Business Trade-offs

For a small application like Task Manager, a monolithic architecture would probably be simpler and less expensive.

The microservice architecture is primarily used to demonstrate cloud computing principles.

For a larger application with many users and different workload patterns, independent scaling and separation of responsibilities could provide greater business value.