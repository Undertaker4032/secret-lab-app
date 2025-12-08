FROM nginx:alpine

# Копирование production конфигурации
COPY nginx.conf /etc/nginx/nginx.conf

# Копирование SSL сертификатов
COPY ssl/ /etc/nginx/ssl/

# Создание директории для логов
RUN mkdir -p /var/log/nginx

# Установка прав для SSL сертификатов
RUN chmod 600 /etc/nginx/ssl/*.key && \
    chmod 644 /etc/nginx/ssl/*.crt

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]