# Expense Tracker

A production-ready Expense Tracker application built with FastAPI, Docker, and Terraform.

## Features
- **Backend**: FastAPI with SQLAlchemy (SQLite/Postgres).
- **Frontend**: Server-Side Rendering with Jinja2 + Bootstrap 5.
- **Charts**: Interactive charts using Chart.js.
- **Infrastructure**: Terraform for AWS EC2 deployment.
- **CI/CD**: Jenkins pipeline for automated testing and deployment.
- **Containerization**: Docker & Docker Compose.

## Quick Start (Local)

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd ExpenseTracker
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   Access the app at `http://localhost:8000`.

3. **Run Manually**:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

## Infrastructure (Terraform)

1. Navigate to `infra/terraform`.
2. Initialize and Apply:
   ```bash
   terraform init
   terraform apply
   ```
3. Note the public IP output.

## CI/CD (Jenkins)

The `Jenkinsfile` defines the pipeline:
1. **Lint**: Checks code quality.
2. **Test**: Runs pytest.
3. **Build**: Builds Docker image.
4. **Deploy**: Deploys to EC2 via SSH.

## Testing

Run unit tests:
```bash
pytest
```
