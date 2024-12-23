from typing import NamedTuple

number = int | float


class RequestDetails(NamedTuple):
    hours: number
    minutes: number
    seconds: number


class SessionDetails(NamedTuple):
    totalSessions: number
    dailySessions: number


class PromptDetails(NamedTuple):
    session: NamedTuple
    minutesPerSession: int
    timePerDay: object
    userDeadline: str
