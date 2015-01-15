FROM texastribune/gunicorn
MAINTAINER tech@texastribune.org

RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update -qq

ADD requirements /app/requirements/
RUN pip install -r /app/requirements/base.txt
RUN pip install -r /app/requirements/production.txt

# ruby for SASS
# node for bower
# git for bower
RUN apt-get -yq install nodejs npm nodejs-legacy ruby git
RUN npm install -g bower
RUN gem install --no-ri --no-rdoc sass

RUN git config --global url."https://".insteadOf git://

ADD bower.json /app/
RUN bower --allow-root install

RUN npm install -g gulp
ADD package.json /app/
RUN npm install

ADD . /app/
ADD gulpfile.js /app/
RUN gulp build:deploy

ENV DJANGO_SETTINGS_MODULE txlege84.settings.production
ENV SECRET_KEY quux
ENV SENTRY_DSN quux
RUN python txlege84/manage.py validate
RUN python txlege84/manage.py collectstatic --noinput
ADD gunicorn.supervisor.conf /etc/supervisor/conf.d/
