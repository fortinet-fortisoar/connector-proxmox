# -*- coding: utf-8 -*-
"""
API Connector Proxmox - FortiSOAR native connector.
Proxmox VE REST API with token authentication.
"""

from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, _check_health

logger = get_logger("API Connector Proxmox")


class ProxmoxApiConnector(Connector):

    def execute(self, config, operation_name, params, **kwargs):
        try:
            params["node"] = params.get("node") or config.get("node")
            params["action"] = operation_name
            op = operations.get(operation_name)
            if not op:
                raise ConnectorError("Unknown operation: {}".format(operation_name))
            logger.info(f"Connectors PARAMETERS >>>>>>>>>>>>>>>>>>>>>: {params}")
            return op(config, params)
        except Exception as e:
            logger.exception("Operation {} failed: {}".format(operation_name, str(e)))
            raise ConnectorError(str(e))

    def check_health(self, config):
        try:
            _check_health(config)
            return True
        except Exception as e:
            logger.exception("check_health failed: {}".format(str(e)))
            raise ConnectorError(str(e))
