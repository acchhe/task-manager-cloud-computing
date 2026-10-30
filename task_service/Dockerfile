# using python 3.13
FROM python:3.13-slim 

# setting/creating working dir inside the container
WORKDIR /app

# copying the requirements needed from requirements.txt to our /app directory
COPY requirements.txt . 

#install the required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]