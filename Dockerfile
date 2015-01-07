FROM texastribune/gunicorn
MAINTAINER tech@texastribune.org

ADD requirements /app/requirements/
RUN pip install -r /app/requirements/base.txt
RUN apt-get update

# ruby for SASS
# node for bower
# git for bower
RUN apt-get -yq install nodejs npm nodejs-legacy ruby git
RUN npm install -g bower
RUN gem install --no-ri --no-rdoc sass

ADD bower.json /app/
RUN bower --allow-root install

# only necessary for dev, I think:
#RUN npm install -g gulp
#ADD package.json /app/
#RUN npm install
