# Simple Text-to-SQL Chatbot

## Backend
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. (Optional) create `backend/.env`:
   ```ini
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=
   MYSQL_DATABASE=edistrict
   ```
3. Run backend:
   ```powershell
   python main.py
   ```

## Frontend
1. Install dependencies:
   ```powershell
   cd ..\frontend
   npm install
   npm run dev
   ```

## Notes
- SQL validation is currently disabled.
- The app uses Ollama to generate SQL and executes it directly against MySQL.
