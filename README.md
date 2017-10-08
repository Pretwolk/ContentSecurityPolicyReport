# ContentSecurityPolicyReport
Parse HTTP CSP reports to ElasticSearch

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
