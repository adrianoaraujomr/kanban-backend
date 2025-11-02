from enum import Enum

class LockReason(str, Enum):
    TOO_HEATED='too heated'
    OFF_TOPIC='off-topic'
    RESOLVED='resolved'
    SPAM='spam'
