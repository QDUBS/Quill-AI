# AI-Driven Text Generation Service

This repository contains a Flask-based application designed to:

- Provide **JWT-secured** endpoints for user authentication and AI-generated text requests.
- Utilize **OpenAI** for text creation based on user inputs.
- Store generated content in a **PostgreSQL** database.
- Support **Docker** and **Docker Compose** for simplified deployment.
- Provide **GitHub Workflow** configuration for managing builds.
- Deploy the application on **AWS** using **Kubernetes - Amazon EKS** and **Amazon ECR**

---

## 1. Introduction

The **AI-Powered Text Generation Service** offers the following capabilities:

- **User Authentication**: Secure login and registration powered by JWT tokens.
- **Text Generation**: Sends prompts to OpenAI’s API for AI-generated content.
- **Text Storage & Management**: Users can view, edit, and delete saved text.
- **PostgreSQL Integration**: SQLAlchemy is used for database management.
- **Containerized Deployment**: Seamless setup with Docker and Docker Compose.
- **Comprehensive Testing**: A pytest-based suite with optional Docker support.
- **Cloud Deployment**: Seamless deployment on Amazon Web Services.

---

## 2. Installation & Configuration

### Environment Variables

The application requires certain environment variables for database credentials, JWT configuration, and OpenAI API access. These can be specified in:

- **`.env`** for development and production
- **`.env.test`** for testing purposes

#### Example `.env` File

```bash
JWT_SECRET=secret
DATABASE_URI='postgresql://postgres:admin@localhost:5433/postgres'
OPENAI_API_KEY=api_key
AWS_ACCESS_KEY_ID=opweejp320020
AWS_SECRET_ACCESS_KEY=secret-access
AWS_REGION=us-west-2
```

#### Example `.env.test` File

```bash
JWT_SECRET=secret
DATABASE_URI='postgresql://postgres:admin@localhost:5433/postgres'
OPENAI_API_KEY=api_key
AWS_ACCESS_KEY_ID=opweejp320020
AWS_SECRET_ACCESS_KEY=secret-access
AWS_REGION=us-west-2
```

## 3. Running the Application

### 3.1 Local Without Docker

1. Ensure PostgreSQL is installed and running.
2. Create a database (e.g., ai_text_gen_db) matching the credentials in .env.
3. Install dependencies within a virtual environment:

```bash
python -m venv quill
source venv/bin/activate
pip install -r requirements.txt
```

4. Start the application:

```bash
python app/main.py
```

5. Access at http://127.0.0.1:5000.

6. Run migrations using alembic
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3.2 Docker Compose (Development)

1. Update .env with your dev environment variables.
2. Run:

```bash
docker compose up --build
```

3. Access at http://localhost:5000.
4. Data Persistence: By default, the Postgres container uses a named volume (e.g., db_data) defined in docker-compose.yml, preserving data across container restarts.

## 4. Testing

### 4.1 Local Testing With a Dedicated Test DB

If you prefer running tests on your host machine:

1. Create a test DB (e.g., `quill_test_db`) in Postgres
2. Install dev dependencies (e.g., pytest):

```bash
pip install -r requirements.txt
```

4. Run:

```bash
pytest --disable-warnings -s
```

This will:

- Load `.env` via `conftest.py` or `pytest-dotenv` (if configured).
- Spin up a Flask test client, connect to the test db, create tables, run all tests, then tear down.


## 5. API Endpoints

Base URL: http://127.0.0.1:5000

1. POST /auth/register
   Request Body:

   ```json
   {
     "username": "confidence",
     "password": "password123"
   }
   ```

   Response: 201 Created on success, 400 if user exists.

2. POST /auth/login
   Request Body:

   ```json
   {
     "username": "confidence",
     "password": "password123"
   }
   ```

   Response: 200 OK with { "access_token": "..." } or 401 on invalid credentials.

3. POST /generate-text (JWT Protected)

   ```json
   {
     "prompt": "How does climate change affect us in 2025. And how can we manage it."
   }
   ```

   Returns a 201 with stored data, or 500 if OpenAI throws an error.

4. GET /generated-text/<id> (JWT Protected)
   Retrieves a response from the db using the ID. Must belong to the user making the request.

5. PUT /generated-text/<id> (JWT Protected)
   Updates prompt and/or response.

6. DELETE /generated-text/<id> (JWT Protected)
   Deletes the stored text.

### JWT Usage:

Send the token in the Authorization header:

```makefile
Authorization: Bearer <access_token>
```

## 6. Deployment (Build via GitHub Workflow and Deploy on AWS)

1. Push a change to the main branch on the GitHub repository.
2. A build is triggered via the script defined in the build.yaml file.
3. Build follows a series of steps to deploy the application on **EKS** using the deployment.yaml file
4. Finally the External IP of the Kubernetes service is returned along with a deployment success message
