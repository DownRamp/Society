FROM python:3.9
WORKDIR /Society

COPY / .
RUN pip install -r requirements.txt
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["./main.py"]
