# Deploy discourse on cloud foundry

This is an MVP for running discourse on cloud foundry. We have branched from the latest discourse release v1.9.2, and then applied some changes so discourse will run on cloud foundry.

It is a work in progress.

## Initial one-off setup on cloud foundry

We assume you have already targeted the application space e.g. `cf target -o myorg -s discourse`.

### Add services to the space

Create postgres and redis services:
```
cf create-service postgres myplan discourse-postgres
cf create-service redis32 myplan discourse-redis
```

### Add secrets
Create a user-provided-service with other secrets.

Rename secrets.sample.json to secrets.json (git ignored), add your secrets, and then run
```
cf cups discourse-ups -p ./secrets.json
```

## Notes for local push using docker images of redis and postgres

Precompiling assets requires services, however these are not available during cloud foundry staging. We will instead precompile assets locally before `cf push`

Start redis and postgres

```
docker run -d --rm -p 5432:5432 --name postgres postgres
docker run -d --rm -p 6379:6379 --name redis redis
```

start container with specific 2.4.1 version from gemfile

```
docker run -it --link postgres:postgres --link redis:redis -v $PWD:/workspace ruby:2.4.1 /bin/bash
```

do ruby things in container to precompile our image assets

```
cd /workspace/
bundle install
export DISCOURSE_REDIS_HOST=redis
export DATABASE_URL=postgres://postgres@postgres:5432/discourse_production
RAILS_ENV=production bundle exec rake db:create
RAILS_ENV=production bundle exec rake assets:precompile
```

cf push will complain about any symlinks present, to resolve this issue:
```
# To find them:
find . -type l -ls | grep "\->"

# delete symlink plugin that doesnt seem necessary
rm public/plugins/discourse-narrative-bot

# Convert symlinks to hard symlinks
find * -type l -exec bash -c 'ln -f "$(greadlink -m "$0")" "$0"' {} \;
```
