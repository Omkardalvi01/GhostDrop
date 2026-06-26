# Stage 1: Build the React application
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy configuration and source files
COPY vite.config.js tailwind.config.js postcss.config.js index.html ./
COPY src/ ./src/

# Build production assets (dist folder)
RUN npm run build

# Stage 2: Serve the application using Caddy
FROM caddy:alpine

# Copy custom Caddy configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Copy build artifacts to Caddy public folder
COPY --from=builder /app/dist /usr/share/caddy

EXPOSE 80
EXPOSE 443
