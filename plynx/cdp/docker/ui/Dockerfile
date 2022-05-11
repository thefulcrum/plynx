FROM node:16-alpine

# Set the working directory to /app
WORKDIR /app

# Copy files
ADD ./ui /app

# Build
ENV NODE_OPTIONS "--max-old-space-size=8192"
