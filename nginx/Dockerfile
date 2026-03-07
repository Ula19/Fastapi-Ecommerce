FROM nginx:1.29-alpine
LABEL authors="ulugbektoshev"

RUN rm /etc/nginx/conf.d/default.conf
COPY fastapi_ecommerce.conf /etc/nginx/conf.d/
