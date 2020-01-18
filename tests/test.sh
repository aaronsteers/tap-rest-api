#/bin/bash

s-tap install tap-rest-api --install_source=./setup.py --plugin_alias=tap-rest-api1
s-tap plan rest-api --config_file=tests/github.secret-config.json --catalog_dir=tests -tap_dir=tests --rescan
s-tap sync rest-api --config_file=tests/github.secret-config.json --catalog_dir=tests -tap_dir=tests
