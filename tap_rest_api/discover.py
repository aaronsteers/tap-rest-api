import os
import requests
import singer
import json
from singer import metadata
import singer.metrics as metrics
import singer.bookmarks as bookmarks


session = requests.Session()
logger = singer.get_logger()

CATALOG_DIR = "catalog"

# TODO: Remove this hardcoded list:

KEY_PROPERTIES = {
    'commits': ['sha'],
    'issues': ['id'],
    'comments': ['id'],
    'assignees': ['id'],
    'collaborators': ['id'],
    'stargazers': ['user_id'],
    'releases': ['id'],
    'pull_requests':['id'],
    'pull_request_reviews': ['id'],
    'pull_request_review_comments': ['id']
}

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    schemas = {}
    for filename in os.listdir(get_abs_path(CATALOG_DIR)):
        path = get_abs_path(CATALOG_DIR) + "/" + filename
        file_raw = filename.replace(".json", "")
        with open(path) as file:
            schemas[file_raw] = json.load(file)
    return schemas


def get_catalog():
    raw_schemas = load_schemas()
    streams = []
    for schema_name, schema in raw_schemas.items():
        # get metadata for each field
        mdata = populate_metadata(schema_name, schema)
        # create and add catalog entry
        catalog_entry = {
            "stream": schema_name,
            "tap_stream_id": schema_name,
            "schema": schema,
            "metadata": metadata.to_list(mdata),
            "key_properties": KEY_PROPERTIES[schema_name],
        }
        streams.append(catalog_entry)
    return {"streams": streams}


def populate_metadata(schema_name, schema):
    mdata = metadata.new()
    # mdata = metadata.write(mdata, (), 'forced-replication-method', KEY_PROPERTIES[schema_name])
    mdata = metadata.write(mdata, (), "table-key-properties", KEY_PROPERTIES[schema_name])
    for field_name in schema["properties"].keys():
        if field_name in KEY_PROPERTIES[schema_name]:
            mdata = metadata.write(
                mdata, ("properties", field_name), "inclusion", "automatic"
            )
        else:
            mdata = metadata.write(
                mdata, ("properties", field_name), "inclusion", "available"
            )
    return mdata


def do_discover():
    catalog = get_catalog()
    # dump catalog
    print(json.dumps(catalog, indent=2))

