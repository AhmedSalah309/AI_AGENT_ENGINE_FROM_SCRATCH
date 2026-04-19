# using python 3.13 as a light base environment
FROM python:3.13-slim

# preventing python from writing .pyc files and enabling logs printing immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# setting the working directory inside the container
WORKDIR /app

# copying and installing libraries first (to benefit from Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copying the rest of the project files
COPY . .

# opening the internal port
EXPOSE 8000

# running gunicorn with 4 workers and threading to support streaming
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:8000", "src.agent_engine.api.main:app"]
