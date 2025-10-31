# MongoDB Optional Mode

This application supports running with or without MongoDB, providing flexibility for different use cases.

## How It Works

### With MongoDB (Default/Production)
- Interview transcripts and feedback are persistently stored in MongoDB
- Data survives server restarts
- Suitable for production environments
- Requires a MongoDB instance (local or cloud like MongoDB Atlas)

### Without MongoDB (Development/Testing)
- Interview transcripts and feedback are stored in-memory
- Data is lost when the server restarts
- No external database setup required
- Perfect for quick testing and development
- Useful for users who want to try the platform without setting up MongoDB

## Configuration

### To Use MongoDB:
Set the `MONGO_URI` in your `backend/src/.env` file:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
```

### To Run Without MongoDB:
Leave `MONGO_URI` empty or comment it out in your `backend/src/.env` file:
```env
MONGO_URI=
# or just omit the line entirely
```

## When to Use Each Mode

### Use MongoDB When:
- Running in production
- Need to persist interview data long-term
- Want to analyze historical interview data
- Multiple users are using the system

### Use In-Memory Storage When:
- Quick local testing and development
- Don't want to set up MongoDB
- Evaluating the platform functionality
- Running demos or workshops
- Data persistence is not required

## Technical Details

The application automatically detects whether MongoDB is configured:
- If `MONGO_URI` is set and not empty: Uses MongoDB
- If `MONGO_URI` is empty or not set: Uses in-memory storage

When the server starts, you'll see a message indicating which mode is active:
- `✓ MongoDB connected` - Using MongoDB
- `⚠ Running without MongoDB - using in-memory storage (data will be lost on restart)` - Using in-memory storage

## Storage Adapter

The implementation uses a `StorageAdapter` class that abstracts database operations, making it transparent to the rest of the application whether MongoDB or in-memory storage is being used.

Located in: `backend/src/database/storage.py`
