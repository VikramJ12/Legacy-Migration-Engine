FROM python:3.12-slim

# System dependencies for pycparser, Neo4j, and build tools
RUN apt-get update && \
    apt-get install -y gcc build-essential libffi-dev curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (override at runtime as needed)
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=strongpass123

# Expose Streamlit default port
EXPOSE 8501

# Default command: run Streamlit app
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
