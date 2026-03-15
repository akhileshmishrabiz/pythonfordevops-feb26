aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin  879381241087.dkr.ecr.ap-south-1.amazonaws.com


879381241087.dkr.ecr.ap-south-1.amazonaws.com/clamav:1.0



docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.13" /bin/sh -c "pip install -r requirements.txt -t python/; exit"
