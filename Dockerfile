FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Set timezone
ENV TZ=Europe/Vienna

# Copy the requiquirements file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the source code to the working directory
COPY . /code

# Expose the port
EXPOSE 8001

# Start the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]