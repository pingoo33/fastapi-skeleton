from datetime import datetime

from fastapi_skeleton.common.consts import TIME_ZONE_KST


def now():
    return datetime.now(TIME_ZONE_KST).replace(tzinfo=None)
