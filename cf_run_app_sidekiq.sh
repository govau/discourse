#!/bin/bash

set -e

eval $(./vcap_services_as_envs.py)

bundle exec sidekiq -e production
