#!/bin/bash

set -e

eval $(./vcap_services_as_envs.py)

bundle exec rake cf:on_first_instance db:migrate && bundle exec rails s -p $PORT -e $RAILS_ENV
