# Build Stage
FROM python:3.9.6-buster AS build
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Final Stage
FROM python:3.9.6-buster
WORKDIR /app

# Copy only the necessary artifacts from the build stage
COPY --from=build /app /app

# Set environment variables
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port
EXPOSE 5000

# Define the command to run on startup
CMD ["python", "-m", "app"]