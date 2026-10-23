# Setup and deployment

## Local setup

You need Python 3 and an OpenAI API key.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install flask openai python-dotenv gunicorn
python3 app.py
```

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask openai python-dotenv gunicorn
python app.py
```

Create a `.env` file in the project root before starting the app:

```text
OPENAI_API_KEY=your_api_key_here
```

Open the local address Flask prints, normally <http://127.0.0.1:5000>.

If PowerShell prevents activation, run this once for the current terminal, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Render deployment

- **Build command:** `pip install flask openai python-dotenv gunicorn`
- **Start command:** `gunicorn app:app --timeout 240`
- **Environment variable:** set `OPENAI_API_KEY` in Render; never commit it to GitHub.

`gunicorn` is for deployment; on Windows, start the app locally with `python app.py`.
