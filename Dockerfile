FROM texastribune/gunicorn
MAINTAINER tech@texastribune.org

RUN apt-get update

ADD requirements /app/requirements/
RUN pip install -r /app/requirements/base.txt
RUN pip install -r /app/requirements/production.txt

# ruby for SASS
# node for bower
# git for bower
RUN apt-get -yq install nodejs npm nodejs-legacy ruby git
RUN npm install -g bower
RUN gem install --no-ri --no-rdoc sass

ADD bower.json /app/
RUN bower --allow-root install

RUN npm install -g gulp
ADD package.json /app/
RUN npm install

ADD txlege84/static /app/
ADD gulpfile.js /app/
RUN gulp build:deploy

ENV DJANGO_SETTINGS_MODULE txlege84.settings.production
ENV SECRET_KEY=quux
ADD . /app/
RUN python txlege84/manage.py validate
RUN python txlege84/manage.py collectstatic --noinput
ADD txlege84/txlege84/wsgi.py /app/
