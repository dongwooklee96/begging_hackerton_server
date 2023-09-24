# Ddip - Backend


### How to Start Server on AWS Ec2 Instance
```bash
# EC2 SSH Connection
# After downloading the PEM key, move to the directory where it's saved
$ sudo ssh -i "ddip.pem" ubuntu@ec2-13-125-131-81.ap-northeast-2.compute.amazonaws.com

# Switch to the root account and navigate to the directory containing the server code
## Error - Check the current directory if this error occurs
## Error loading ASGI app. Could not import module "main". ##
$ sudo -i 
$ cd ddip-server/

# Start server
$ uvicorn main:app

################# Note #################
# Due to the absence of CI/CD implementation, if any changes happen on Git repository, it is necessary to pull the code
$ git pull

# Stop and restart nginx server
$ service nginx restart

# Nginx environment setting file
$ cd
$ vi /etc/nginx/sites-enabled/default

# Fast api environmet setting file
$ cd
$ vi /etc/nginx/sites-enabled/fastapi_nginx

```





