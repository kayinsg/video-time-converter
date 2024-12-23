import module
from InputUtils import getTimeInputFromUser, askMinutesPerSession, askDeadlineFromUser
from core import Sessions
from dataComponents import PromptDetails, SessionDetails
from messageToUser import introductionToProgram

print(introductionToProgram)
timeFromUser: str = getTimeInputFromUser()
totalRawMinutes: int = module.gatherTimeFromUserInMinutes(timeFromUser)
minutesPerSession: int = askMinutesPerSession()
session: Sessions = Sessions(
    totalRawMinutes,
    minutesPerSession
)


userDeadline: str = askDeadlineFromUser()
daysBeforeDeadline: int = module.computeDaysBeforeDeadline(userDeadline)
sessionDetails: SessionDetails = module.handleTotalSessionDetails(
    session,
    daysBeforeDeadline
)
dailyTime: object = module.handleDailyTimeDetails(
    session,
    sessionDetails
)


prompt = PromptDetails(
    sessionDetails,
    minutesPerSession,
    dailyTime,
    userDeadline
)


timePrompts: list = module.instantiateTimePrompts(prompt)
module.printTimeDetails(timePrompts)
