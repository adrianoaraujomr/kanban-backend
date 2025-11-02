from enum import Enum

class IssueState(str, Enum):
    OPEN='open',
    CLOSED='closed'

class IssueStateReason(str, Enum):
    COMPLETED='completed'
    NOT_PLANNED='not_planned'
    DUPLICATE='duplicate'
    REOPENED='reopened'