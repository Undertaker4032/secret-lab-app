FROM node:22-alpine

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm ci

COPY ./frontend/ ./

RUN npm run build

RUN ls -la build/ && test -f build/index.js

EXPOSE 3000

CMD ["node", "build/index.js"]