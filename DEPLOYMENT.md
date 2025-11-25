# Deployment Guide - External Database

## Option 1: Deploy with External Database (No RDS)

### Method A: Using CDK Context

```bash
cd /Users/miguepoloc/Code/seynurwa/infrastructure/cdk

# Deploy simple stack (no RDS)
cdk deploy AuthStackSimple \
  -c use_external_db=true \
  -c database_url="postgresql+asyncpg://user:pass@your-db.com:5432/authdb"
```

### Method B: Set DATABASE_URL After Deployment

```bash
# 1. Deploy the simple stack
cdk deploy AuthStackSimple -c use_external_db=true

# 2. Update Lambda environment variable via AWS CLI
aws lambda update-function-configuration \
  --function-name AuthStackSimple-AuthLambda-xxxxx \
  --environment "Variables={
    DATABASE_URL=postgresql+asyncpg://user:pass@your-db.com:5432/authdb,
    JWT_EXPIRATION_HOURS=24
  }"

# 3. Or update via AWS Console:
# AWS Console → Lambda → Your function → Configuration → Environment variables
```

### Method C: Use Secrets Manager for Database URL

```bash
# 1. Create secret for database URL
aws secretsmanager create-secret \
  --name auth/database-url \
  --secret-string "postgresql+asyncpg://user:pass@your-db.com:5432/authdb"

# 2. Get the secret ARN
aws secretsmanager describe-secret --secret-id auth/database-url

# 3. Grant Lambda permission and update code to read from Secrets Manager
```

---

## Option 2: Deploy with RDS Included

```bash
cd /Users/miguepoloc/Code/seynurwa/infrastructure/cdk

# Deploy full stack with RDS
cdk deploy AuthStack
```

---

## Local Testing

### Quick Start (Docker PostgreSQL)

```bash
# 1. Start PostgreSQL
docker run --name auth-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=authdb \
  -p 5432:5432 \
  -d postgres:15

# 2. Setup environment
cd /Users/miguepoloc/Code/seynurwa/modules/auth_v2
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/authdb"
export JWT_SECRET="local-dev-secret"

# 3. Run migrations
alembic upgrade head

# 4. Start server
PYTHONPATH=../.. uvicorn handler:app --reload
```

### Connect to External Database

```bash
# Point to your existing database
export DATABASE_URL="postgresql+asyncpg://user:pass@your-db.com:5432/authdb"
export JWT_SECRET="your-jwt-secret"

cd /Users/miguepoloc/Code/seynurwa/modules/auth_v2
alembic upgrade head
PYTHONPATH=../.. uvicorn handler:app --reload
```

---

## Testing

```bash
# Test local
curl http://localhost:8000/health

curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"pass1234"}'

# Test AWS (after deployment)
ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name AuthStackSimple \
  --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue' \
  --output text)

curl $ENDPOINT/health
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret for signing JWT tokens |
| `JWT_EXPIRATION_HOURS` | No | Token expiration (default: 24) |

---

## Database Migration

After deploying to AWS, run migrations:

```bash
# Option A: From local machine (if DB is accessible)
export DATABASE_URL="postgresql+asyncpg://user:pass@your-db.com:5432/authdb"
cd /Users/miguepoloc/Code/seynurwa/modules/auth_v2
alembic upgrade head

# Option B: Use AWS Lambda to run migrations
# Create a separate Lambda function that runs: alembic upgrade head
```
