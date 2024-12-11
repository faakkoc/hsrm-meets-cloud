FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx

COPY container01/hsrm.html /var/www/html/index.html

CMD ["nginx", "-g", "daemon off;"]