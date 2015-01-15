FROM texastribune/gunicorn
MAINTAINER tech@texastribune.org

RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update -qq

ADD requirements /app/requirements/
RUN pip install --quiet -r /app/requirements/base.txt
RUN pip install --quiet -r /app/requirements/production.txt

# - the null redirection will catch the still-noisy stdout but errors
# will still be echoed
# - ruby for SASS, node and git for bower
RUN apt-get -y -qq install nodejs ruby git > /dev/null
RUN npm install --silent --quiet -g bower > /dev/null
RUN gem install --no-ri --no-rdoc sass

RUN git config --global url."https://".insteadOf git://

ADD bower.json /app/
RUN bower --quiet --allow-root install

RUN npm install --silent -g gulp > /dev/null
ADD package.json /app/
RUN npm install --silent > /dev/null

ADD . /app/
ADD gulpfile.js /app/
RUN gulp build:deploy

ENV DJANGO_SETTINGS_MODULE txlege84.settings.production
ENV SECRET_KEY quux
ENV SENTRY_DSN quux
RUN python txlege84/manage.py validate
RUN python txlege84/manage.py collectstatic --verbosity=0 --noinput
ADD gunicorn.supervisor.conf /etc/supervisor/conf.d/
