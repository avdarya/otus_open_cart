FROM agridyaev/opencart:4.0.2-3-debian-12-r33
RUN echo "Mutex posixsem" >> /opt/bitnami/apache/conf/httpd.conf
