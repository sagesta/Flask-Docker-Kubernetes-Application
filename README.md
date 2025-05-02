# Flask + Docker + Kubernetes Application

A production-ready Flask application setup with Docker containerization and Kubernetes orchestration.

## 📋 Overview

This repository contains everything you need to deploy a scalable Flask web application with PostgreSQL database using Docker for containerization and Kubernetes for orchestration. Perfect for microservices architecture and cloud-native applications.

## 🏗️ Project Structure

```
flask-app/
├── app.py               # Main Flask application
├── Dockerfile           # Docker configuration for Flask app
└── requirements.txt     # Python dependencies

K8s/
├── configmap.yaml           # ConfigMap for non-sensitive configuration
├── flask-deployment.yaml    # Deployment configuration for Flask app
├── ingress.yaml             # Ingress for external access
├── postgres.deployment.yaml # Deployment configuration for Postgres
└── secret.yaml              # Secret for sensitive configuration
```

## 🔧 Setup & Configuration

### Flask Application

The Flask application connects to PostgreSQL and provides basic endpoints including a health check for Kubernetes probes.

**Key Features:**
- PostgreSQL database integration
- Environment variable configuration
- Health check endpoint for Kubernetes
- Database connection test endpoint

### Requirements

```
Flask==2.3.3
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

## 🐳 Docker Setup

### Build the Docker Image

```bash
cd flask-app
docker build -t mypyapp:latest .
```

### Create Docker Network

```bash
docker network create my-app-network
```

### Run PostgreSQL Container

```bash
docker run -d \
  --name postgres-db \
  --network my-app-network \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:13
```

### Run Flask Application Container

```bash
docker run -d \
  --name mypyapp \
  --network my-app-network \
  -e POSTGRES_HOST=postgres-db \
  -e POSTGRES_DB=mydatabase \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -p 5000:5000 \
  mypyapp
```

## ☸️ Kubernetes Deployment

### Create Namespace

```bash
kubectl create namespace dev-app
```

### Deploy Application Stack

Apply the Kubernetes configurations in the following order:

```bash
# 1. Apply ConfigMap and Secret
kubectl apply -f K8s/configmap.yaml
kubectl apply -f K8s/secret.yaml

# 2. Deploy PostgreSQL database
kubectl apply -f K8s/postgres.deployment.yaml

# 3. Deploy Flask application
kubectl apply -f K8s/flask-deployment.yaml

# 4. Apply Ingress for external access
kubectl apply -f K8s/ingress.yaml
```

### Verify Deployment

```bash
# Check if pods are running
kubectl get pods -n dev-app

# Check services
kubectl get services -n dev-app

# Check deployments
kubectl get deployments -n dev-app
```

## 🔍 Kubernetes Configuration Details

### ConfigMap (configmap.yaml)
Contains non-sensitive configuration settings for the application:
- PostgreSQL host information
- Database name
- Application environment settings

### Secret (secret.yaml)
Stores sensitive information securely:
- Database credentials (username and password)

### PostgreSQL Deployment (postgres.deployment.yaml)
Sets up a PostgreSQL database with:
- Persistent volume for data storage
- Environment variables from ConfigMap and Secret
- Headless service for internal access

### Flask Deployment (flask-deployment.yaml)
Deploys the Flask application with:
- Multiple replicas for high availability
- Resource constraints (CPU and memory)
- Liveness and readiness probes
- Environment variables from ConfigMap and Secret

### Ingress (ingress.yaml)
Configures external access to the application:
- Host-based routing
- Path configurations
- Integration with ingress controller

## 🛠️ Monitoring & Troubleshooting

### View Pod Logs

```bash
kubectl logs -n dev-app <pod-name>
# Example: kubectl logs -n dev-app flask-app-58ff9dd79b-pz2nz
```

### Check Pod Details

```bash
kubectl describe pod -n dev-app <pod-name>
```

### Port Forwarding for Testing

```bash
kubectl port-forward -n dev-app service/flask-service 8080:80
```

### Exec into Pod

```bash
kubectl exec -it -n dev-app <pod-name> -- /bin/bash
```

## 📊 Scaling

Scale the Flask application deployment:

```bash
kubectl scale -n dev-app deployment/flask-app --replicas=5
```

## 🔄 CI/CD Integration

This setup can be integrated with CI/CD pipelines:

1. Build Docker image in CI pipeline
2. Push to container registry
3. Update Kubernetes deployment with new image
4. Apply configuration changes if needed

## 📝 Configuration Details

The Kubernetes configuration files are carefully structured to:
- Separate concerns (application, database, networking)
- Follow best practices for security (using Secrets)
- Enable easy scaling and maintenance
- Provide health monitoring through probes

## 🔒 Security Considerations

- Database credentials stored in Kubernetes Secrets
- Network policies can be added for additional security
- Resource limits prevent resource exhaustion
- Probes ensure application health

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

