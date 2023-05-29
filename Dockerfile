FROM python:3.8.10-slim-buster AS builder

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY app /app
COPY dbAPI /app/dbAPI

## Add the wait script to the image
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait


# Install packages from requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
RUN chmod +x /app/launch.sh

# ENV PYTHONPATH "${PYTHONPATH}:/dbAPI"

EXPOSE 5000

# ENTRYPOINT ["python3"]
# CMD ["app.py"]
CMD /wait && /app/launch.sh