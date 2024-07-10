# API FAST DNS BLACKLIST review

### Api version APIFAST

### Generate file Variables of environment

```bash
cat > env.txt << EOF
ENVIRONMENT=production
EOF
```

## Build on local instance

`docker build -f Dockerfile -t backend-dnsbl --no-cache .`

## Running Docker 

`docker run -di -p 8080:8080 -v $(pwd)/src/:/opt/back_dnsrbl --env-file ./env.txt --name backend-dnsbl  -d backend-dnsbl`

## Command inspect

`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' backend-dnsbl`

`docker exec -ti backend-dnsbl bash`

## Try execute with:

* http://0.0.0.0:8080/docs
* http://127.0.0.1:8080/docs
* http://localhost:8080/docs

### Run backend without Docker

`python /opt/disk_balancer/api.py`

### Restart fastapi in Docker
`supervisorctl restart fast`

### Stop fastapi
`supervisorctl stop fast`

## Command execute Demon

Command for stablish blacklist:

`host -W 2 -t a ip-alreves.dnsbl`

`host -W 2 -t a 1.112.64.186.sbl-xbl.spamhaus.org`