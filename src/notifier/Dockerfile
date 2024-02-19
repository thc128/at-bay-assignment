FROM asaf-base

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5681 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "handler.py"]
