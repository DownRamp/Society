# To Run
## Docker
docker build -t reporting-app:latest .
docker run -p 8501:8501 reporting-app:latest
will be at: localhost:8501

## Local 
pip install -r requirements.txt
streamlit run main.py