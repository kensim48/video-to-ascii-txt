aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 277965450838.dkr.ecr.ap-southeast-1.amazonaws.com
docker build -t video-to-ascii .
docker tag video-to-ascii:latest 277965450838.dkr.ecr.ap-southeast-1.amazonaws.com/video-to-ascii:latest
docker push 277965450838.dkr.ecr.ap-southeast-1.amazonaws.com/video-to-ascii:latest