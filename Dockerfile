# Start from a clean, slim Python 3.13 base image
FROM python:3.13-slim
# Work inside a folder called /app
WORKDIR /app
# Copy the dependency list in first, then install it.
# Doing this before the rest lets Docker reuse the install
# step unless the dependencies actually change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application in
COPY . .
# The app listens on this port
ENV PORT=5000
EXPOSE 5000
# How to start the app
CMD ["python", "-m", "app.main"]