#!/usr/bin/env python

import os
import json
import sys

for service in json.loads(os.environ.get("VCAP_SERVICES", "{}")).get("postgres", []):
    for k, v in service.get("credentials", {}).items():
        sys.stdout.write('export DISCOURSE_DB_%s="$(printf -- %s)"\n' % (k.upper(), repr(str(v))))

for service in json.loads(os.environ.get("VCAP_SERVICES", "{}")).get("redis32", []):
    for k, v in service.get("credentials", {}).items():
        sys.stdout.write('export DISCOURSE_REDIS_%s="$(printf -- %s)"\n' % (k.upper(), repr(str(v))))

for service in json.loads(os.environ.get("VCAP_SERVICES", "{}")).get("user-provided", []):
    for k, v in service.get("credentials", {}).items():
        sys.stdout.write('export %s="$(printf -- %s)"\n' % (k, repr(str(v))))
