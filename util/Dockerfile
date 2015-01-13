FROM texastribune/txlege84
MAINTAINER tech@texastribune.org

#
# Build via:
#   docker build -t txlege84-util .

RUN pip install postdoc
RUN apt-get update
RUN apt-get install -yq pv postgresql-client

# the base image specifies an ENTRYPOINT so this returns it to the default:
ENTRYPOINT ["/bin/sh","-c"]
