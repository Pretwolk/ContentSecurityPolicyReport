# ContentSecurityPolicyReport
Parse HTTP CSP reports to ElasticSearch

CONTEXT
This python3 API takes the Content Security Policy reporting POST from a browser and adds it to the configured Elasticsearch cluster.

Read https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP#Enabling_reporting before using this API

The API does some basic checks if the POSTer is a normal browser and it expects the proper HTTP headers. Nothing witholds an adversary to craft a valid request and poison your data. 

TODO
- Add configurable settings
- Add demo screenshots to github
- Add IP blacklisting/throtteling
- Add server side threading

INSTALL
```
apt install python3-pip python3-venv
useradd -r -s /bin/false cspreporting
git clone https://github.com/Pretwolk/ContentSecurityPolicyReport.git /opt/ContentSecurityPolicyReport 
python3 -m venv /opt/ContentSecurityPolicyReport
cd /opt/ContentSecurityPolicyReport
source bin/activate
pip3 install -r requirements.txt
chown -R cspreporting:cspreporting /opt/ContentSecurityPolicyReport
cp /opt/ContentSecurityPolicyReport/init/systemd.service /etc/systemd/system/ContentSecurityPolicyReport.service
systemctl daemon-reload
systemctl enable ContentSecurityPolicyReport
systemctl start ContentSecurityPolicyReport
```

CONFIG
Still need to implement

RUNNING 
Nginx config example 
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name SERVER_HOSTNAME;

    root /var/www/;
    index index.html;

    ssl_certificate PATH_TO_CERT; 
    ssl_certificate_key PATH_TO_PRIVKEY; 

    location /api/v1/csp/ {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header Front-End-Https on;
        proxy_pass http://[::1]:8080;
    }
}
```
