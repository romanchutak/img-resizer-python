FROM nginx

# RUN rm /etc/nginx/nginx.conf

# COPY resizer.conf /etc/nginx/templates/resizer.conf.template
# COPY nginx.conf /etc/nginx/templates/nginx.conf.template

COPY resizer.conf /etc/nginx/templates/default.conf.template

EXPOSE 8091

# CMD ["nginx", "-g", "'daemon off;'"]
