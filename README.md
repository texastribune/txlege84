# txlege84

The lege app to end all lege apps.

## Requirements

- Django 1.7
- [virtualenv/virtualenvwrapper](http://virtualenvwrapper.readthedocs.org)
- [Node/npm](http://nodejs.org)
  - [Gulp](http://gulpjs.com)
- [Bower](http://bower.io)
- [Sass + Ruby](http://sass-lang.com)

## Getting started

Please note – this guide assumes you are using OS X. If you aren't, you hopefully know the equivalent commands to make these things happen. If you don't, find someone to help you!

First, clone the project.

```bash
git clone https://github.com/texastribune/txlege84.git
```

Then, create the virtual environment for your project.

```bash
mkvirtualenv txlege84-dev
```

Don't forget to activate it!

```bash
workon txlege84-dev
```

Next, install the Python development requirements.

```bash
pip install -r requirements/local.txt
```

Once that finishes, run the initial migration, then try to run the project!

```bash
python txlege84/manage.py migrate
python txlege84/manage.py runserver
```

You should be able to check the site out at [`http://localhost:8000`](), but it's gonna look funky. Time to set up styling!

First, we install all our `node` and `bower` dependencies.

```bash
npm install && bower install
```

This project uses `gulp` to run `scss` compiling and other various tasks.

Now here's where the magic happens. Gulp uses [BrowserSync](http://www.browsersync.io) to handle live reloading of the page during development. So when you're working on the front end, you'll need two terminal windows or tabs.

In the first, you'll run the Django `runserver` command.

```bash
python txlege84/manage.py runserver
```

In the second, you'll run the `gulp` serve command.

```bash
gulp serve
```

This routes the Django's development server through BrowserSync's development server, so whenever anything changes with the templates or styles the page reloads automatically.

With both of those running, visit [`http://localhost:3000`]() to view the site.

Now get to work!

## Bootstrapping the data for development

You'll need a [Sunlight Foundation API key](http://sunlightfoundation.com/api/accounts/register/) to run these steps. Once you have it, you'll need to add it to your environment. There are a number of ways to do that, but the easiest way is:

```bash
export SUNLIGHT_API_KEY=<api-key-characters>
```

Next, you need to prep your database.

```bash
python txlege84/manage.py migrate
```

Then, run the make command to load the data.

```bash
make prep_for_development
```

## Docker

Here's how to set up the database with Docker. You'll need to do this to get an updated database from the Sunlight Foundation.

First, start-up docker: `boot2docker up`

If you get an error, run `docker ps` to make sure there aren't conflicts with other running containers. Run `docker stop [container_id]` to shut down other containers.

Next, create your .env file, and add your DATABASE_URL to that file:

`export DATABASE_URL=postgres://docker:docker@docker.local:5432/docker`

Run `source .env` after creating the file.

Then refresh your database, `make docker/refresh-db`.





