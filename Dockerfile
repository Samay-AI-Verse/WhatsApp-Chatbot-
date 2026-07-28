# Step 1: Use an official lightweight Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the requirements file first
# This is a Docker Best Practice called "Caching Layers"
COPY requirements.txt .

# Step 4: Install the dependencies
# --no-cache-dir keeps the container image size small and clean
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Expose port 8000 (FastAPI default, but Render will override this dynamically)
EXPOSE 8000

# Step 7: The command to run your FastAPI app
# We use sh -c to expand ${PORT:-8000} dynamically. 
# This ensures it binds to Render's dynamic PORT environment variable (usually 10000) 
# while still falling back to 8000 when running locally.
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
