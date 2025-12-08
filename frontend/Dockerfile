FROM node:22-alpine

WORKDIR /app

# Копирование package файлов
COPY package*.json ./
RUN npm ci

# Копирование исходного кода
COPY . .

# Убедимся что adapter-node установлен
RUN npm install @sveltejs/adapter-node

# Сборка приложения
RUN npm run build

EXPOSE 3000

# Запуск приложения
CMD ["node", "build"]