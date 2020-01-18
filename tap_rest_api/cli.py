"""
The CLI entrypoint for the tap
"""

import singer

from . import discover
from . import sync

REQUIRED_CONFIG_KEYS = ["access_token", "endpoints"]

logger = singer.get_logger()

@singer.utils.handle_top_exception(logger)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    if args.discover:
        discover.do_discover()
    else:
        if args.catalog:
            logger.info("Received catalog from 'catalog' argument")
            catalog = args.catalog.to_dict()
        elif args.properties:
            logger.info("Received catalog from 'properties' argument")
            catalog = args.properties
        else:
            logger.info("Received catalog from discover")
            catalog = discover.get_catalog()
        sync.do_sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
