# Satellite Monitoring Application

A full-stack application for monitoring Areas of Interest (AOI) using satellite data. Users can define geographic areas and receive alerts about changes like deforestation, construction, or other land use modifications.

## Features

### Frontend (React + TypeScript)
- **Authentication**: Secure user registration and login
- **Interactive Map**: Draw polygons and rectangles to define AOIs
- **Dashboard**: Overview of all AOIs with status and monitoring information
- **AOI Management**: Create, view, edit, and delete Areas of Interest
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Backend (FastAPI + MongoDB)
- **REST API**: Complete CRUD operations for users and AOIs
- **JWT Authentication**: Secure token-based authentication
- **MongoDB Integration**: Efficient data storage and retrieval
- **Data Validation**: Comprehensive input validation using Pydantic

## Tech Stack

### Frontend
- React 18 with TypeScript
- React Router for navigation
- Leaflet.js with React-Leaflet for interactive maps
- Tailwind CSS for styling
- Axios for API communication
- React Hook Form for form handling
- React Hot Toast for notifications

### Backend
- FastAPI (Python)
- MongoDB with Motor (async driver)
- JWT for authentication
- BCrypt for password hashing
- Pydantic for data validation

## Project Structure

```
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── contexts/        # React contexts (Auth)
│   │   ├── pages/          # Page components
│   │   └── App.tsx         # Main app component
│   └── package.json
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── README.md
└── README.md
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- MongoDB

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running on your system

5. Start the FastAPI server:
```bash
python main.py
```

The backend API will be available at `http://localhost:8000`

## Usage

1. **Sign Up**: Create a new account or log in with existing credentials
2. **Dashboard**: View overview of your AOIs and monitoring statistics
3. **Create AOI**: Use the interactive map to draw areas you want to monitor
4. **Configure Monitoring**: Set monitoring frequency, change types, and notification preferences
5. **Manage AOIs**: View, edit, or delete your existing Areas of Interest

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation when the backend is running.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.