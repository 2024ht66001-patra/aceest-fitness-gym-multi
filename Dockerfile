FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Use a real app object so flask can start consistently inside the container
# FLASK_APP uses the pattern module:callable (flask_app.py -> app object)
ENV FLASK_APP=flask_app:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
EXPOSE 5000
# Use the flask CLI to run on the internal port 5000 bound to all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
