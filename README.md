# Railway PaaS Clone

A full-stack Platform-as-a-Service (PaaS) clone inspired by Railway.app, built with modern web technologies.

## Overview

Railway PaaS Clone is a monorepo project that replicates the core functionality of Railway.app, a popular deployment platform. It provides a complete solution for deploying, managing, and scaling applications with an intuitive web interface and powerful CLI.

## Architecture

This is a monorepo project with the following structure:

```
railway-paas-clone/
├── backend/           # FastAPI application (Python)
├── frontend/          # Next.js application (TypeScript/React)
├── cli/              # Python CLI tool
├── scripts/          # Utility scripts
├── docs/             # Documentation
├── docker-compose.yml # Development services
├── package.json      # Root workspace configuration
├── .gitignore
├── .editorconfig
└── README.md
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context / Zustand
- **Package Manager**: npm (via bun)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Process Manager**: PM2

### Infrastructure
- **Reverse Proxy**: Traefik
- **Container Runtime**: Docker (for dev dependencies only)
- **Deployment**: Process-based (PM2), not containerized

### CLI
- **Language**: Python
- **Package Manager**: pip

## Prerequisites

- Node.js 18+ (with bun package manager)
- Python 3.11+
- Docker & Docker Compose
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd railway-paas-clone
```

### 2. Start Development Services

```bash
npm run docker:up
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Traefik Dashboard (http://traefik.localhost:8080)

### 3. Install Dependencies

```bash
# Install root dependencies
npm install

# Install workspace dependencies
npm install -w frontend
npm install -w cli
```

### 4. Set Up Environment Variables

Create `.env.local` files in each workspace:

**frontend/.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**backend/.env**
```
DATABASE_URL=postgresql://railway:railway_dev_password@localhost:5432/railway_dev
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
```

### 5. Run Development Servers

```bash
# Run all services concurrently
npm run dev

# Or run individually
npm run dev -w frontend  # Next.js on http://localhost:3000
npm run dev -w cli       # CLI development
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Traefik Dashboard**: http://traefik.localhost:8080

## Development Commands

```bash
# Install dependencies
npm install

# Start development servers
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run linting
npm run lint

# Docker Compose commands
npm run docker:up      # Start services
npm run docker:down    # Stop services
npm run docker:logs    # View logs
```

## Project Structure Details

### Backend (`backend/`)
FastAPI application handling:
- User authentication & authorization
- Application management
- Deployment orchestration
- Database operations
- API endpoints

### Frontend (`frontend/`)
Next.js application providing:
- Dashboard UI
- Application management interface
- Deployment history
- User settings
- Real-time logs

### CLI (`cli/`)
Python CLI tool for:
- Local development
- Deployment management
- Configuration
- Authentication

### Scripts (`scripts/`)
Utility scripts for:
- Database migrations
- Seed data
- Deployment helpers
- Maintenance tasks

### Docs (`docs/`)
Documentation including:
- API documentation
- Architecture guides
- Deployment guides
- Contributing guidelines

## Database Schema

The application uses PostgreSQL with the following main entities:
- Users
- Teams
- Projects
- Applications
- Deployments
- Environments
- Services

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `ENVIRONMENT`: dev/staging/production

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_APP_NAME`: Application name

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `npm run test`
4. Run linting: `npm run lint`
5. Commit with clear messages
6. Push to your branch
7. Create a Pull Request

## Code Style

- **JavaScript/TypeScript**: ESLint + Prettier
- **Python**: Black + isort + flake8
- **EditorConfig**: Configured for consistent formatting

## Deployment

### Development
```bash
npm run docker:up
npm run dev
```

### Production
- Backend: Deploy with PM2
- Frontend: Build and deploy to Vercel or similar
- Database: Managed PostgreSQL instance
- Cache: Managed Redis instance

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port
lsof -ti:5432 | xargs kill -9
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Reset database
npm run docker:down
npm run docker:up
```

### Redis Connection Issues
```bash
# Check Redis is running
docker-compose logs redis

# Test connection
redis-cli ping
```

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] User authentication system
- [ ] Application deployment
- [ ] Real-time logs
- [ ] Environment management
- [ ] Team collaboration
- [ ] API integrations
- [ ] Monitoring & alerts
- [ ] Auto-scaling
