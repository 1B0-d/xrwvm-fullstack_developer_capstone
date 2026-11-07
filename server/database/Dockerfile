FROM node:22-slim

ENV NODE_ENV=production
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY data/dealerships.json data/reviews.json ./
COPY app.js dealership.js inventory.js review.js ./

EXPOSE 3030
CMD ["node", "app.js"]
