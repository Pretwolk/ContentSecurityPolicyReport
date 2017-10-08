# ContentSecurityPolicyReport
Parse HTTP CSP reports to ElasticSearch

INSTALL
```
sudo useradd -r -s /bin/false cspreporting
sudo mkdir /opt/ContentSecurityPolicyReport
sudo chown cspreporting:cspreporting /opt/ContentSecurityPolicyReport

sudo -u cspreporting git clone https://github.com/Pretwolk/ContentSecurityPolicyReport.git /opt/ContentSecurityPolicyReport 
sudo cp /opt/ContentSecurityPolicyReport/init/systemd.service /etc/systemd/system/ContentSecurityPolicyReport.service
sudo systemctl daemon-reload
sudo systemctl enable ContentSecurityPolicyReport
sudo systemctl start ContentSecurityPolicyReport
```

CONFIG
Still need to implement
