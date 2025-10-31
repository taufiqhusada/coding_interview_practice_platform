# interview_tool_frontend



## Project Setup

```sh
npm install
```

### Environment Configuration

Configure environment variables:
```sh
cp .env.example .env
# Edit .env file with your backend URL
```

Create a `.env` file in the `frontend/` directory with:
```env
VITE_BACKEND_URL=http://127.0.0.1:5000
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## Code Structure
- main vue code is in `src/App.vue`
- each components is on `src/components/`
