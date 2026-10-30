# Task Manager - Cloud Computing Project

## Overview

Task Manager is a cloud-native application built with Python, FastAPI, MongoDB, Docker, and Kubernetes.

The application consists of two independently scalable REST API microservices and a persistent database.

## Technologies

- Python
- FastAPI
- MongoDB
- Docker
- Kubernetes

## Microservices

### Task Service

Provides REST endpoints for creating, reading, updating, and deleting tasks.

### Statistics Service

Retrieves task data from Task Service and calculates task statistics.

## Architecture

The application contains three main components:

- Task Service: 2 replicas
- Statistics Service: 2 replicas
- MongoDB: 1 replica with persistent storage

For more information, see [Architecture Documentation](architecture/architecture.md).


## Installation and Deployment

### Prerequisites

Before deploying the application, make sure you have:

- Docker Desktop
- Kubernetes enabled in Docker Desktop
- kubectl installed and configured

### Deploy to Kubernetes

Navigate to the `kubernetes` directory:

```powershell
cd kubernetes
```

Deploy all Kubernetes resources:

```powershell
kubectl apply -f .
```

Verify that the Deployments are running:

```powershell
kubectl get deployments
```

Verify the Kubernetes Services:

```powershell
kubectl get services
```

### Access the APIs

When running with Docker Desktop Kubernetes, the APIs can be accessed at:

- Task Service: http://localhost:8000/docs
- Statistics Service: http://localhost:8001/docs

These localhost addresses depend on the local Kubernetes environment and LoadBalancer support.