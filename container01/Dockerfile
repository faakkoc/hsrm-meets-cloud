FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx

COPY container01/hsrm.html /var/www/html/index.html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]