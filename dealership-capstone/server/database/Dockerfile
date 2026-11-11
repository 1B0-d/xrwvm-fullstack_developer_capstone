FROM node:22-slim

ENV NODE_ENV=production
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY data ./data
COPY app.js seed.js dealership.js inventory.js review.js ./

EXPOSE 3030
CMD ["node", "app.js"]
