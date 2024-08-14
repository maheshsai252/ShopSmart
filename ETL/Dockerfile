FROM apache/airflow
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Add script to the container image
# COPY create_conn.sh /create_conn.sh

# Set execute permissions on the script
# RUN chmod +x /create_conn.sh

