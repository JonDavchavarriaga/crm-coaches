# CRM Core Service

CRM Core Service built with Python 3.11, FastAPI, and Hexagonal Architecture (Ports and Adapters).

---

## Overview

The **CRM Core Service** manages coaches, clients, sessions, and goals within a clean, decoupled architecture. By adhering to **Hexagonal Architecture (Ports & Adapters)**, the core domain logic remains isolated from external frameworks, infrastructure drivers, and AWS cloud dependencies.

---

## Architecture

```text
+-------------------------------------------------------------------------------+
|                            INFRASTRUCTURE LAYER                               |
|                                                                               |
|   +-----------------------+                    +--------------------------+   |
|   |   FastAPI REST API    |                    |   DynamoDB Repository    |   |
|   |   (Driving / Inbound) |                    |   (Driven / Outbound)    |   |
|   +-----------+-----------+                    +------------^-------------+   |
+---------------|---------------------------------------------|-----------------+
                | (HTTP Requests / DTOs)                      | (Implements Port)
                v                                             |
+-------------------------------------------------------------|-----------------+
|                            APPLICATION LAYER                |                 |
|                                                             |                 |
|   +---------------------------------------------------------+-------------+   |
|   |                        ClientService                                  |   |
|   |   - Orchestrates use cases (Create Client, Get Client by ID)          |   |
|   +---------------------------------------+-------------------------------+   |
+-------------------------------------------|-----------------------------------+
                                            | (Invokes & Coordinates)
                                            v
+-------------------------------------------------------------------------------+
|                              DOMAIN LAYER                                     |
|                                                                               |
|   +--------------------------+                 +--------------------------+   |
|   |      Domain Models       |                 |       Port Interfaces    |   |
|   |  - Client, Coach, Goal   | <-------------- |  - ClientRepository      |   |
|   |  - Pure Business Rules   |                 |    (Abstract Interface)  |   |
|   +--------------------------+                 +--------------------------+   |
+-------------------------------------------------------------------------------+
```

---

## Tech Stack

- **Runtime & Language**: Python 3.11
- **Web Framework**: FastAPI
- **Data Validation & Settings**: Pydantic v2
- **AWS SDK**: Boto3
- **Containerization**: Docker & Docker Compose
- **Infrastructure as Code (IaC)**: Terraform
- **Cloud Emulation**: LocalStack Pro (DynamoDB, SQS, S3)

---

## Quickstart Guide

Follow these 3 steps to set up, launch, and verify the microservice locally:

### 1. Provision Infrastructure
Initialize and provision the required AWS resources (DynamoDB table, SQS queue, S3 bucket) using Terraform and LocalStack:
```bash
cd terraform && terraform init && terraform apply -auto-approve && cd ..
```

### 2. Start Microservice
Build the container image and spin up the FastAPI service in detached mode:
```bash
docker compose up -d --build
```

### 3. Run Integration Tests
Grant execution permissions and run the end-to-end integration test suite:
```bash
chmod +x ./scripts/test-endpoints.sh && ./scripts/test-endpoints.sh
```

---

## API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health status check | `200 OK` |
| `POST` | `/clients/` | Create and persist a new client entity | `201 Created` |
| `GET` | `/clients/{id}` | Retrieve client details by unique ID | `200 OK` / `404 Not Found` |

---

## Interactive Documentation

Once the service is running, interactive API documentation is accessible at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
