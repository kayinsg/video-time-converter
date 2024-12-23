import core
from dataComponents import SessionDetails


def gatherTimeFromUserInMinutes(unformattedTimeFromUser) -> int:
    timeComponents = core.Request().getIndividualTimeFromUser(
        unformattedTimeFromUser
    )
    timeFromUserInMinutes = core.TimeConverter(
        timeComponents
    ).getTimeComponent("minutes")
    return timeFromUserInMinutes


def computeDaysBeforeDeadline(userDeadline) -> int:
    date = core.Date()
    pendulumDeadline = date.encodeUserDeadline(userDeadline)
    daysBeforeDeadline = date.computeDaysTillDeadline(pendulumDeadline)
    return daysBeforeDeadline


def handleTotalSessionDetails(session, daysBeforeDeadline):
    totalSessions = session.calculateTotalSessions()
    dailySessions = session.calculateSessionsPerDay(daysBeforeDeadline)
    return SessionDetails(totalSessions, dailySessions)


def handleDailyTimeDetails(
    session: core.Sessions, sessionDetails: SessionDetails
) -> object:
    minutesPerSession = session.minutesPerSession
    dailySessions = sessionDetails.dailySessions
    dailySeconds = minutesPerSession * dailySessions * 60
    dailyTime = core.DailyTimeCalculator(
        0, 0, dailySeconds
    ).calculateHoursFromSeconds()
    return dailyTime


def instantiateTimePrompts(promptDetails) -> list[core.PrinterInterface]:
    totalSessions = promptDetails.session.totalSessions
    dailySessions = promptDetails.session.dailySessions
    minutesPerSession = promptDetails.minutesPerSession
    timePerDay = promptDetails.timePerDay
    userDeadline = promptDetails.userDeadline

    timePrompts = [
        core.TotalSessions(totalSessions, minutesPerSession),
        core.DailySessions(dailySessions, userDeadline),
        core.DailyTime(
            timePerDay.hours, timePerDay.minutes, timePerDay.seconds
        ),
    ]
    return timePrompts


def printTimeDetails(timePrompts):
    printManager = core.PrinterContext(timePrompts)
    printManager.displayDetailsToUser()
