
#upstream pingpong {
#   ip_hash;
##  server unix:/var/nginx/uwsgi.sock;
#   server 127.0.0.1:8080;
#}


server {
    listen   80; ## listen for ipv4; this line is default and implied
    #listen   [::]:80 default ipv6only=on; ## listen for ipv6

    root /home/baden/new.navi.cc/www;
    index index.html index.htm;

    # Make site accessible from http://new.navi.cc/
    server_name new.navi.cc;
    server_name *.new.navi.cc;

    expires 1M; # yes one month

    # Static assets
    location ~* ^.+\.(manifest|appcache)$ {
        expires -1;
        #access_log logs/static.log;
    }

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to index.html
        rewrite ^(.*)#.*$ $1;
        try_files $uri $uri.html $uri/ /index.html;
    }

    location /gcm {
        proxy_set_header X-Real-IP  $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Port 80;
        proxy_pass http://localhost:8084;
#       proxy_redirect default;
#       proxy_redirect off;
#       proxy_redirect http://localhost:8000/api/ http://localhost/api/;
    }

    location ~* /(verify|process|affiliate|auth) {
#   location /process {
#   location /verify {
        proxy_pass http://localhost:8001;
    }

    #error_page 404 /404.html;

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #   deny all;
    #}
    add_header "X-UA-Compatible" "IE=Edge,chrome=1";
}

