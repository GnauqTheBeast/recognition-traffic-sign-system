🚀 Spring Boot Microservices on Kubernetes
This project showcases a microservices architecture built with Spring Boot, orchestrated by Spring Cloud, and deployed on Kubernetes (K8s). It includes a React frontend and a PostgreSQL database for a complete cloud-native application.
🛠️ Components

🧭 Eureka Server: Service registry for microservice discovery.
🌐 API Gateway: Centralized routing with Spring Cloud Gateway.
📦 Microservices:
traffic-sign-service: Handles traffic sign-related functionality.
user-service: Manages user data and operations.


🗃️ PostgreSQL Database: Persistent storage for microservices.
🌈 React Frontend (react-app): User interface for interacting with the backend.


### 📁 Project Structure
<pre>
microservices/
├── eureka-server/          # Service registry using Eureka for service discovery
├── api-gateway/            # API Gateway for routing requests to the appropriate microservices
├── traffic-sign-service/   # Microservice for managing traffic signs
├── user-service/           # Microservice for managing user data
├── react-app/              # Frontend application developed with React
├── k8s/                    # Kubernetes manifests for deploying the application
└── README.md               # Documentation for the project
</pre>

✅ Prerequisites
Ensure the following tools are installed:

🐳 Docker: For building and running container images.
☸️ Kubernetes: Local (Minikube, Docker Desktop) or cloud-based (EKS, GKE, AKS).
🛠️ kubectl: Kubernetes command-line tool.
🔨 Maven: For building Spring Boot applications (Gradle optional).
📟 Node.js: For building the React frontend (v16 or later recommended).

Optional:

🐙 Docker Hub account: For pushing and pulling images.


⚙️ Step-by-Step: Deploy to Kubernetes
Follow these steps to build, deploy, and run the application on Kubernetes.
1. Clone the Repository
git clone <repository-url>
cd microservices

2. Build Docker Images
Navigate to each Spring Boot project directory and build the Docker images:
# Build Spring Boot services
<pre>
cd eureka-server
./mvnw clean package -DskipTests
docker build -t your-dockerhub/eureka-server .

cd ../api-gateway
./mvnw clean package -DskipTests
docker build -t your-dockerhub/api-gateway .

cd ../traffic-sign-service
./mvnw clean package -DskipTests
docker build -t your-dockerhub/traffic-sign-service .

cd ../user-service
./mvnw clean package -DskipTests
docker build -t your-dockerhub/user-service .
</pre>

# Build React frontend
<pre>
cd ../react-app
npm install
npm run build
docker build -t your-dockerhub/react-app .
</pre>

Note: Replace your-dockerhub with your Docker Hub username or registry.
3. Push Images to Docker Hub (Optional)
If deploying to a remote Kubernetes cluster, push the images to a registry:
<pre>
docker push your-dockerhub/eureka-server
docker push your-dockerhub/api-gateway
docker push your-dockerhub/traffic-sign-service
docker push your-dockerhub/user-service
docker push your-dockerhub/react-app
</pre>

4. Deploy to Kubernetes
Apply the Kubernetes manifests to deploy the application:
<pre>
kubectl apply -f k8s/

Note: Ensure your k8s/ directory contains all necessary YAML files (e.g., postgres.yaml, eureka-server.yaml, etc.). If a single manifest.yaml file is used, run:
kubectl apply -f k8s/manifest.yaml
</pre>
5. Verify Deployment
Check the status of pods, services, and deployments:
kubectl get pods
kubectl get services
kubectl get deployments

Access the application:

React Frontend: Use the service URL or port-forward to react-app (e.g., kubectl port-forward svc/react-app 3000:80).
API Gateway: Port-forward to test API endpoints (e.g., kubectl port-forward svc/api-gateway 8080:80).


🔄 Redeploying After Code Changes
To update the application after modifying backend or frontend code:
1. Clean Up Existing Resources
Delete existing deployments and services to avoid conflicts:
<pre>
kubectl delete deployment postgres eureka-server api-gateway traffic-sign-service user-service react-app
kubectl delete service postgres eureka-server api-gateway traffic-sign-service user-service react-app
</pre>

2. Rebuild Applications
For each Spring Boot service:

cd <service-directory>
./mvnw clean install -DskipTests

For the React frontend:
cd react-app
npm install
npm run build

3. Rebuild Docker Images
Rebuild the Docker images for all components:
<pre>
docker build -t your-dockerhub/eureka-server ./eureka-server
docker build -t your-dockerhub/api-gateway ./api-gateway
docker build -t your-dockerhub/traffic-sign-service ./traffic-sign-service
docker build -t your-dockerhub/user-service ./user-service
docker build -t your-dockerhub/react-app ./react-app
Note: If using Minikube, ensure you're still using its Docker daemon (eval $(minikube docker-env)).
</pre>

Push updated images to Docker Hub (if needed):
<pre>
docker push your-dockerhub/eureka-server
docker push your-dockerhub/api-gateway
docker push your-dockerhub/traffic-sign-service
docker push your-dockerhub/user-service
docker push your-dockerhub/react-app
</pre>
4. Reapply Kubernetes Configuration
Redeploy the application:
<pre>
kubectl apply -f k8s/manifest.yaml
</pre>

🛠️ Troubleshooting

Pods not starting: Check logs with kubectl logs <pod-name>.
Service not accessible: Verify service type (e.g., ClusterIP, NodePort, LoadBalancer) and port configuration.
Database issues: Ensure PostgreSQL credentials and connection strings are correct in k8s/postgres.yaml.
Image pull errors: Confirm Docker Hub credentials and image tags.


📚 Additional Resources

Spring Boot Documentation
Spring Cloud Documentation
Kubernetes Documentation
Minikube Setup
Docker Hub


🤝 Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.
