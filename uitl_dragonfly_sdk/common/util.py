from uitl_dragonfly_sdk.common.DragonflyException import DragonflyException


def verify_mandatory_param(param: str, name: str) -> None:
    if not param:
        raise DragonflyException("Mandatory parameter missing: {}", name)


DRAGONFLY_API_HEALTH_REPORT_URL = "/api/health-reports"
DEFAULT_MIN_DCR = 95.0
