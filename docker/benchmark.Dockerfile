# Use a lightweight Ubuntu base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install  \
    git \
    build-essential \
	unzip \
	curl \
    libssl-dev -y 

WORKDIR /home
RUN git config --global http.version HTTP/1.1

RUN git clone https://github.com/wg/wrk.git wrk && \
    cd wrk && \
	make

# Run the wrk benchmark command
CMD ["wrk", "-t10", "-c10", "http://host.docker.internal:8080"]