FROM httpd:alpine
# COPY ./public_html/ /usr/local/apache2/htdocs/
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf
RUN cd /usr/local/apache2/htdocs && find . -type f -print0 | xargs -0 chmod 666
RUN cd /usr/local/apache2/htdocs && find . -type d -print0 | xargs -0 chmod 777