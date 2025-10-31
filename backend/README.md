## How to Setup
1. Install Python 3
2. `pip install -r requirements.txt`
3. Configure environment variables:
   ```bash
   cd src
   cp .env.example .env
   # Edit .env file with your credentials
   ```

## Environment Variables
Create a `.env` file in the `backend/src/` directory with the following variables:

**Option 1: With MongoDB (Recommended for Production)**
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_GPT_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your_jwt_secret_key_here
```

> 📚 **New to MongoDB?** Follow this [MongoDB Atlas Tutorial](https://www.mongodb.com/resources/products/platform/mongodb-atlas-tutorial) for easy setup. Atlas offers a free tier perfect for getting started!

**Option 2: Without MongoDB (Development/Testing)**
```env
# Leave MONGO_URI empty to use in-memory storage
MONGO_URI=
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_GPT_MODEL=gpt-4o-mini
JWT_SECRET_KEY=your_jwt_secret_key_here
```

> **Note:** When `MONGO_URI` is empty or not set, the application uses in-memory storage. Interview data will be lost when the server restarts.

## How to run
1. `flask --app src/app run`  
2. Usually it will run on `http://127.0.0.1:5000`

## Code Structure
- main program is on `src/app.py`
- all function implementations is on `src/routes/`
