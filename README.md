# 🛰️ Project Bolt: Satellite Change Detection Platform

> **Monitor environmental changes in real-time with satellite imagery and intelligent change detection**

Project Bolt is a comprehensive full-stack web application that leverages Google Earth Engine to monitor and visualize satellite-detected changes over user-defined Areas of Interest (AOIs). Built for researchers, environmental scientists, and organizations who need to track land use changes, deforestation, urban development, and other environmental transformations.

## 📊 Process Flow Diagram

![Process Flow](https://github.com/P47Parzival/LISS-4-Satellite-imagery/blob/main/Images/image1.png?raw=true)

---

## 😄 Model Analysis

![Analysis](https://github.com/P47Parzival/LISS-4-Satellite-imagery/blob/main/Images/image2.png?raw=true)

---

## 🖼️ Before & After: Change Detection Example

<table>
  <tr>
    <td align="center"><b>Before</b></td>
    <td align="center"><b>After</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/P47Parzival/LISS-4-Satellite-imagery/blob/main/Images/image_before.png?raw=true" width="250"/></td>
    <td><img src="https://github.com/P47Parzival/LISS-4-Satellite-imagery/blob/main/Images/image_after.png?raw=true" width="250"/></td>
  </tr>
  <h3>Reason: Urbanization<h3>
</table>


## ✨ Key Features

### 🔐 **Secure User Management**
- JWT-based authentication with HTTP-only cookies
- Secure user registration and login system
- Session management and protection

### 🗺️ **Area of Interest (AOI) Management**
- Interactive map interface for defining monitoring areas
- CRUD operations for AOI management
- Geospatial data validation and storage

### 🚨 **Intelligent Change Detection**
- Automated satellite image analysis using Google Earth Engine
- Real-time change detection alerts
- Historical alert tracking and management
- Customizable detection sensitivity

### 🖼️ **Satellite Image Streaming**
- On-demand "before" and "after" satellite image thumbnails
- Secure image streaming via Google Earth Engine
- High-resolution imagery from multiple satellite sources

### 💻 **Modern User Interface**
- Responsive React-based frontend
- Clean, intuitive design with Tailwind CSS
- Real-time updates and notifications
- Mobile-friendly interface

## 🛠️ Tech Stack

| Component                     | Technology                                              |
|-------------------------------|-------------------------------------------------------- |
| **Frontend**                  | ⚛️ React 18, 📘 TypeScript, 🎨 Tailwind CSS            |
| **Backend**                   | ⚡ FastAPI (Python 3.8+)                                |
| **Database**                  | 🍃 MongoDB                                              |
| **Satellite Data (prototype)**| 🛰️ Google Earth Engine Python API                       |
| **Authentication**            | 🔐 JWT with HTTP-only cookies                           |
| **HTTP Client**               | 📡 Axios                                                |
| **Task Queue**                | 🌱 Celery (worker & client)                             |
| **Cache/Broker**              | 🔴 Redis                                                |
| **Additional**                | 🌐 CORS, 📤 StreamingResponse, 🗺️ Geospatial libraries |

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **MongoDB** ([Installation Guide](https://docs.mongodb.com/manual/installation/))
- **Google Earth Engine Account** ([Sign up](https://earthengine.google.com/))

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/yourusername/project-bolt.git
cd project-bolt/project
```

### 2. 🔧 Backend Setup

#### Install Dependencies
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

#### Configure Google Earth Engine
```bash
# Authenticate with Google Earth Engine
python -c "import ee; ee.Authenticate()"
```
Follow the authentication flow in your browser.

#### Environment Configuration
Create a `.env` file in the `backend` directory:
```env
# Database
MONGODB_URL=mongodb://localhost:27017/project_bolt

# JWT Configuration
JWT_SECRET_KEY=your_super_secure_secret_key_here
JWT_ALGORITHM=HS256

# Google Earth Engine
GEE_SERVICE_ACCOUNT_KEY=path/to/your/service-account-key.json

# API Configuration
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

#### Start the Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 3. 🖥️ Frontend Setup

#### Install Dependencies
```bash
cd ../frontend
npm install
```

#### Environment Configuration
Create a `.env` file in the `frontend` directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_MAP_API_KEY=your_map_api_key_here
```

#### Start the Development Server
```bash
npm start
```

The application will open at `http://localhost:3000`

### 4. 🗄️ Database Setup

Ensure MongoDB is running on your system:
```bash
# macOS (with Homebrew)
brew services start mongodb-community

# Ubuntu/Debian
sudo systemctl start mongod

# Windows
net start MongoDB
```

### 5. ⚡ Start Celery Worker and Beat

In a new terminal (from the `backend` directory, with your virtual environment activated):

#### Start the Celery worker and beat in backend terminal:
```bash
celery -A main.celery_app worker --loglevel=info

celery -A main.celery_app beat --loglevel=info

```


---

## 📁 Project Structure

```
project-bolt/
├── 📂 backend/
│   ├── 📄 main.py                 # FastAPI application entry point
│   ├── 📄 routes_auth.py          # Authentication endpoints
│   ├── 📄 routes_aoi.py           # AOI management endpoints
│   ├── 📄 routes_alerts.py        # Change detection alerts
│   ├── 📄 database.py             # MongoDB connection and models
│   ├── 📄 gee_integration.py      # Google Earth Engine integration
│   ├── 📄 auth_utils.py           # JWT and authentication utilities
│   ├── 📄 requirements.txt        # Python dependencies
│   └── 📄 .env                    # Environment variables
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── 📄 AOIAlertsModal.tsx
│   │   │   ├── 📄 MapComponent.tsx
│   │   │   ├── 📄 AuthForm.tsx
│   │   │   └── 📄 Dashboard.tsx
│   │   ├── 📂 hooks/
│   │   ├── 📂 utils/
│   │   ├── 📄 App.tsx
│   │   └── 📄 index.tsx
│   ├── 📄 package.json
│   └── 📄 .env
├── 📂 docs/                       # Additional documentation
├── 📄 README.md
└── 📄 docker-compose.yml          # Docker configuration (optional)
```

---

## 🔧 Configuration

### Google Earth Engine Setup

1. **Create a Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Earth Engine API**
   - Enable the Google Earth Engine API for your project
   - Create a service account and download the JSON key

3. **Set up Authentication**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

### MongoDB Configuration

For production deployments, consider using MongoDB Atlas:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/project_bolt
```

---

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Manual Deployment

#### Backend (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### Frontend (Build for Production)
```bash
npm run build
# Serve the build folder with your preferred web server
```

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/signup` | User registration |
| `POST` | `/auth/login` | User authentication |
| `GET` | `/aoi/list` | List user's AOIs |
| `POST` | `/aoi/create` | Create new AOI |
| `GET` | `/alerts/{aoi_id}` | Get change detection alerts |
| `GET` | `/thumbnails/{alert_id}` | Stream satellite thumbnails |

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all new frontend components
- Add tests for new features
- Update documentation as needed

---

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Verify Google Earth Engine authentication
python -c "import ee; ee.Initialize()"
```

**Frontend build errors:**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Database connection issues:**
- Ensure MongoDB is running
- Check connection string in `.env` file
- Verify network connectivity

### Getting Help

- 🐛 [Report Issues](https://github.com/P47Parzival/LISS-4-Satellite-imagery/issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Earth Engine** for satellite imagery and analysis capabilities
- **FastAPI** team for the excellent web framework
- **React** and **Tailwind CSS** communities
- All contributors and users of this project

---

## 📊 Project Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![React](https://img.shields.io/badge/react-18.0+-blue)

---

**Built with ❤️ for environmental monitoring and change detection**