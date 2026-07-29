# Replacement Index — Championship CB Recruitment Tool

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:8501

## Deploy on Render
1. Push this folder to a GitHub repo
2. New Web Service on Render, connect the repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
