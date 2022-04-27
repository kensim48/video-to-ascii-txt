FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY web_pre.html ${LAMBDA_TASK_ROOT}
COPY web_post.html ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
# RUN yum check-update
RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum install -y jp2a libgl1-mesa-glx libglib2.0-0
RUN yum install -y epel-release
RUN yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
RUN yum install -y libwayland-client    
RUN rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
RUN yum localinstall -y --nogpgcheck http://mirror.centos.org/centos/7/os/x86_64/Packages/libva-1.8.3-1.el7.x86_64.rpm 
RUN yum install -y ffmpeg ffmpeg-devel
RUN yum install libXext libSM libXrender
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 