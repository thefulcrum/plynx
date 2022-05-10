FROM node:16-alpine

# Set the working directory to /app
WORKDIR /app

# Copy files
ADD ./ui/README.md                  /app
ADD ./ui/generate-build-version.js  /app
ADD ./ui/package-lock.json          /app
ADD ./ui/package.json               /app
ADD ./ui/public                     /app/public
ADD ./ui/src                        /app/src

# Copy licence
ADD ./LICENSE /app

# Build
ENV NODE_OPTIONS "--max-old-space-size=8192"
