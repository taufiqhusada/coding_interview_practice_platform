# Conversational AI for Technical Interview Practice

A web-based platform that uses conversational AI to help Computer Science students practice the think-aloud process during technical interviews. This system was developed as part of the research presented in the paper "Designing Conversational AI to Support Think-Aloud Practice in Technical Interview Preparation for CS Students" published at **IEEE VL/HCC 2025**.
- **Paper**: [arXiv:2507.14418](https://arxiv.org/abs/2507.14418)
- **Conference**: IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC) 2025

## 🎯 Overview

Technical interviews are crucial for CS students, but the think-aloud process—where candidates verbalize their thought processes while solving coding problems—remains challenging to practice. This platform addresses this gap by providing an LLM-based conversational AI system that offers:

- **Techincal Interview Simulation**: AI-facilitated mock interview tool that simulates a technical interview experience through  voice-based natural conversation
- **AI Feedback on Think-Aloud Practice**: Providing feedback on users’ think-aloud performance based on the interview simulation (A) transcript
- **AI-Generated Think-Aloud Example Dialogue**: Providing (A) AI-generated dialogues that model thinking aloud during a technical interview for each coding problem. The goal is to help users learn from examples relevant to their current task and better articulate their thought processes

![Interview Simulation](public/1_interview%20simulation.png)


![Feedback System](public/2_feedback.png)


![Learning Examples](public/3_example.png)




## 🛠️ Technology Stack

### Backend
- **Python Flask** - Web framework with async support
- **OpenAI API** - Large Language Model integration
- **MongoDB** (Optional) - Database for storing sessions and user data
  - Can run without MongoDB using in-memory storage for development/testing


### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript development
- **CodeMirror 6** - Advanced code editor with syntax highlighting
- **Bootstrap 5** - Responsive UI framework
- **Axios** - HTTP client for API requests

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **OpenAI API Key** (Required)
- **MongoDB** (Optional - for persistent storage. Without it, data is stored in-memory and lost on restart)

> 💡 **New Feature**: The platform now supports running without MongoDB! See [MONGODB_OPTIONAL.md](MONGODB_OPTIONAL.md) for more details.


## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/coding_interview_practice_platform.git
cd coding_interview_practice_platform
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cd src
cp .env.example .env
# Edit .env file with your API keys and database URLs
cd ..
```

**Configure the backend `.env` file** (`backend/src/.env`):

**Option 1: With MongoDB (Recommended for Production)**
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_GPT_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your_jwt_secret_key_here
```

**Option 2: Without MongoDB (Development/Testing)**
```env
# Leave MONGO_URI empty or comment it out to use in-memory storage
MONGO_URI=
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_GPT_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your_jwt_secret_key_here
```

> **Note:** When running without MongoDB, interview transcripts and feedback are stored in memory and will be lost when the server restarts. This mode is suitable for development and testing only.

### 3. Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env file with your backend API URL
```

**Configure the frontend `.env` file** (`frontend/.env`):
```env
VITE_BACKEND_URL=http://127.0.0.1:5000
```

## 🚀 Running the Application

### Development Mode

1. **Start the Backend Server**:
   ```bash
   cd backend
   flask --app src/app run
   # Server runs on http://127.0.0.1:5000
   ```

2. **Start the Frontend Development Server**:
   ```bash
   cd frontend
   npm run dev
   # Application runs on http://localhost:5173
   ```

### Production Build

1. **Build the Frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy Backend**:
   ```bash
   cd backend
   # Use the provided deploy.sh script or deploy manually
   gunicorn --bind 0.0.0.0:5000 src.app:app
   ```

## 📁 Project Structure

```
coding_interview_practice_platform/
├── backend/                    # Flask backend application
│   ├── src/
│   │   ├── app.py             # Main Flask application
│   │   └── routes/            # API route implementations
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   └── deploy.sh             # Deployment script
├── frontend/                  # Vue.js frontend application
│   ├── src/
│   │   ├── App.vue           # Main Vue application
│   │   └── components/       # Vue components
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Vite build configuration
└── public/                   # Static assets and documentation images
    ├── 1_interview simulation.png
    ├── 2_feedback.png
    └── 3_example.png
```


## 📝 Citation

If you use this platform in your research or find it helpful, please cite our paper:

```bibtex
@inproceedings{daryanto2025designing,
  title={Designing Conversational AI to Support Think-Aloud Practice in Technical Interview Preparation for CS Students},
  author={Daryanto, Taufiq and Stil, Sophia and Ding, Xiaohan and Manesh, Daniel and Lee, Sang Won and Lee, Tim and Lunn, Stephanie and Rodriguez, Sarah and Brown, Chris and Rho, Eugenia},
  booktitle={2025 IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC)},
  year={2025},
  organization={IEEE}
}
```


## 📞 Contact

For questions about this research or the platform, please contact:

- **Taufiq Daryanto** - [Email](mailto:taufiqhd@vt.edu)

## 🔗 Links

- **Paper**: [arXiv:2507.14418](https://arxiv.org/abs/2507.14418)
- **Conference**: [IEEE VL/HCC 2025](https://conf.researchr.org/home/vlhcc-2025)

---

