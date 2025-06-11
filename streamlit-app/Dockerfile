FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
# Copy the content directory
COPY content ./content

EXPOSE 8501

ENV STREAMLIT_SERVER_ADDRESS="0.0.0.0"
ENV STREAMLIT_SERVER_PORT="8501"
ENV STREAMLIT_SERVER_ENABLE_CORS="true"
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION="false"

CMD ["streamlit", "run", "app.py"]
