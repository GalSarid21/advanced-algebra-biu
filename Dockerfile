FROM python:3.12-bookworm
WORKDIR /app

# Create a non-root user (1000:1000)
RUN addgroup --gid 1000 appgroup && \
    adduser --uid 1000 --gid 1000 --disabled-password --gecos "" appuser

# Create logs directory
RUN mkdir -p /app/logs && chown appuser:appgroup /app/logs

# Create a virtual environment
RUN pip install --upgrade pip setuptools
RUN python -m venv /app/venv

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy project fiels
COPY task_manager /app/task_manager
COPY common /app/common
COPY data /app/data
COPY src /app/src
COPY main.py /app/main.py

# Set premissions and switch to new appuser
RUN chown -R 1000:1000 /app
USER appuser

ENV TASK="run-all"
ENTRYPOINT ["/bin/sh", "-c", "/app/venv/bin/python main.py --task $TASK"]