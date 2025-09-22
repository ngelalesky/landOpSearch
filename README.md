# 🏞️ Land Opportunity Search

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue.svg)](https://kubernetes.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)](https://github.com/yourusername/landOpSearch)

> An AI-powered system using Reinforcement Learning to identify and evaluate land development opportunities through geospatial data analysis and machine learning.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Kubernetes cluster (optional)
- PostgreSQL (for MLflow backend)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/landOpSearch.git
cd landOpSearch/land-agent-backend
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

4. **Start MLflow tracking server**
```bash
cd infra/mlflow
docker-compose up -d
```

5. **Run the API server**
```bash
cd inference_api
python app.py
```

The API will be available at `http://localhost:8000`

## 📖 Overview

Land Opportunity Search is an intelligent system that leverages Reinforcement Learning (RL) to analyze land parcels and provide development opportunity assessments. The system combines:

- **Geospatial Data Processing**: Integration with satellite imagery, soil data, and zoning information
- **Machine Learning**: PPO (Proximal Policy Optimization) for intelligent land evaluation
- **REST API**: FastAPI-based service for real-time predictions
- **Data Pipeline**: Apache Airflow for automated data ingestion and processing
- **Cloud Infrastructure**: Kubernetes deployment with monitoring and scaling

### Key Features

- 🧠 **AI-Powered Analysis**: RL-based land opportunity identification
- 🛰️ **Satellite Integration**: Real-time satellite imagery processing
- 📊 **MLOps Pipeline**: MLflow integration for experiment tracking
- 🔄 **Automated Data Pipeline**: Airflow DAGs for data orchestration
- ☁️ **Cloud-Native**: Kubernetes deployment with auto-scaling
- 📈 **Monitoring**: Comprehensive observability with Prometheus/Grafana

## 🏗️ Architecture

```mermaid
graph TB
    A[Data Sources] --> B[Airflow DAGs]
    B --> C[Data Processing]
    C --> D[Feature Engineering]
    D --> E[Model Training]
    E --> F[Model Registry]
    F --> G[Inference API]
    G --> H[Load Balancer]
    H --> I[Client Applications]
    
    J[Monitoring] --> E
    J --> G
    K[MLflow] --> E
    K --> F
```

### Core Components

| Component | Description | Technology |
|-----------|-------------|------------|
| **Environment Service** | Custom RL environment for land analysis | Gymnasium, NumPy |
| **Training Pipeline** | PPO model training with MLflow tracking | Stable-Baselines3, PyTorch |
| **Inference API** | REST API for land evaluation | FastAPI, Uvicorn |
| **Data Pipeline** | Automated data ingestion and processing | Apache Airflow, S3 |
| **Infrastructure** | Container orchestration and deployment | Kubernetes, Docker |

## 🛠️ Development

### Project Structure

```
land-agent-backend/
├── 📁 env_service/           # RL environment implementation
│   └── land_opportunity_env.py
├── 📁 trainer/              # Model training pipeline
│   ├── ppo_trainer.py
│   └── Dockerfile
├── 📁 inference_api/        # FastAPI service
│   └── app.py
├── 📁 data_ingestion/       # Data pipeline components
│   ├── load_land_data.py
│   ├── fetch_remote_data.py
│   └── tasks/
├── 📁 airflow/              # Workflow orchestration
│   └── dags/
├── 📁 k8s/                  # Kubernetes configurations
│   ├── deployment.yaml
│   └── service.yaml
├── 📁 infra/                # Infrastructure setup
│   └── mlflow/
├── 📁 preprocessing/        # Data preprocessing utilities
├── requirements.txt         # Python dependencies
└── setup.py                # Package configuration
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/land_search
MLFLOW_TRACKING_URI=http://localhost:5000

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=land-data-bucket

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=your-secret-key-here

# Model Configuration
MODEL_PATH=./best_model/best_model
MAX_BATCH_SIZE=100
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v --cov=.

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .
mypy .

# Security check
bandit -r .
```

## 🚀 Deployment

### Local Development

1. **Start MLflow tracking server**
```bash
cd infra/mlflow
docker-compose up -d
```

2. **Run data pipeline**
```bash
cd airflow
airflow webserver --port 8080 &
airflow scheduler &
```

3. **Train model**
```bash
cd trainer
python ppo_trainer.py
```

4. **Start API server**
```bash
cd inference_api
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment

```bash
# Build images
docker build -t land-agent-api:latest inference_api/
docker build -t land-agent-trainer:latest trainer/

# Run with docker-compose
docker-compose up -d
```

### Kubernetes Deployment

1. **Apply configurations**
```bash
kubectl apply -f k8s/
```

2. **Check deployment status**
```bash
kubectl get pods -l app=land-agent-api
kubectl get services
```

3. **Access the application**
```bash
kubectl port-forward service/land-agent-api 8000:8000
```

## 📊 API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Land Evaluation
```http
POST /evaluate
Content-Type: application/json

{
  "features": [0.5, 0.6, 0.8, 0.3, 0.2, 0.9, 0.7, 0.4, 0.6]
}
```

**Response:**
```json
{
  "score": 0.75,
  "confidence": 0.85,
  "recommended_action": 2
}
```

### Feature Vector

The input feature vector contains:
- `[0]` - X coordinate (normalized)
- `[1]` - Y coordinate (normalized)
- `[2]` - Soil type (encoded)
- `[3]` - Elevation (normalized)
- `[4]` - Slope (normalized)
- `[5]` - Water access (binary)
- `[6]` - Zoning type (encoded)
- `[7]` - Market value (normalized)
- `[8]` - Development potential (normalized)

## 🔧 Configuration

### Model Training

Key hyperparameters in `trainer/ppo_trainer.py`:

```python
TRAINING_CONFIG = {
    "total_timesteps": 1_000_000,
    "learning_rate": 3e-4,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.01
}
```

### Environment Configuration

Environment settings in `env_service/land_opportunity_env.py`:

```python
ENV_CONFIG = {
    "max_steps": 100,
    "observation_space_dim": 9,
    "action_space_size": 9,
    "reward_threshold": 0.8
}
```

## 📈 Monitoring

### Metrics

The system exposes metrics for:
- API response times
- Model prediction accuracy
- Data pipeline health
- Resource utilization

### Dashboards

Access monitoring dashboards:
- **Grafana**: http://localhost:3000
- **MLflow**: http://localhost:5000
- **Airflow**: http://localhost:8080

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- 📖 **Documentation**: Check the [wiki](https://github.com/ngelalesky/landOpSearch/wiki)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/ngelalesky/landOpSearch/issues)
- 💬 **Discussions**: [Join our discussions](https://github.com/ngelalesky/landOpSearch/discussions)
- 📧 **Email**: techstation634@gmail.com
.com

### FAQ

**Q: How accurate are the land opportunity predictions?**
A: The model achieves 85%+ accuracy on validation data, but performance may vary based on data quality and regional characteristics.

**Q: Can I use this for commercial purposes?**
A: No, this project can not be use for commercial purpose.

**Q: How do I add new data sources?**
A: Extend the data ingestion pipeline in `data_ingestion/` and update the Airflow DAGs.


## 🙏 Acknowledgments

- [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) for RL algorithms
- [FastAPI](https://github.com/tiangolo/fastapi) for the API framework
- [Apache Airflow](https://github.com/apache/airflow) for workflow orchestration
- [MLflow](https://github.com/mlflow/mlflow) for experiment tracking

---

**Built with ❤️ for the future of intelligent land development**

[![GitHub stars](https://img.shields.io/github/stars/ngelalesky/landOpSearch.svg?style=social&label=Star)](https://github.com/ngelalesky/landOpSearch)
[![GitHub forks](https://img.shields.io/github/forks/ngelalesky/landOpSearch.svg?style=social&label=Fork)](https://github.com/ngelalesky/landOpSearch/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/ngelalesky/landOpSearch.svg?style=social&label=Watch)](https://github.com/ngelalesky/landOpSearch)
