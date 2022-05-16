# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

import os
from pathlib import Path
from typing import Dict, Any, Optional

import yaml


_cdp_config = None


def get_config(config_file: Optional[str] = None, service: Optional[str] = None) -> Dict[str, Any]:
    """Create or return config per service if specified, otherwise return the entire config."""

    global _cdp_config

    if _cdp_config is None:

        if not config_file:
            # use default
            config_file = os.path.join(
                Path(__file__).parent.parent.parent, "config.yaml"
            )

        with open(config_file) as f:
            _cdp_config = yaml.load(f, Loader=yaml.FullLoader)

    return _cdp_config[service] if service else _cdp_config


get_config()
