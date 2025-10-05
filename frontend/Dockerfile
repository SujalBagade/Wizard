FROM node:20-alpine

WORKDIR /app

# Copy package.json first for caching
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the code
COPY . .

EXPOSE 3000

# Run the dev server
CMD ["npx", "next", "dev", "-p", "3000"]
