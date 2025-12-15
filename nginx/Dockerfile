FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY ssl/ /etc/nginx/ssl/

RUN mkdir -p /var/log/nginx

RUN chmod 600 /etc/nginx/ssl/*.key && \
    chmod 644 /etc/nginx/ssl/*.crt

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]