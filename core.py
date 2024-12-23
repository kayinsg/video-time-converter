import math
from typing import NamedTuple
import pendulum
from abc import ABC, abstractmethod
from Exceptions import InvalidDateFromUserError
from Exceptions import InvalidTimeInputError
from dataComponents import RequestDetails

number = int | float


class Request:
    """
    The central objective of following functions is to prompt the user to
    Enter input.
    """

    def __init__(self, hours=0, minutes=0, seconds=0) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def getIndividualTimeFromUser(self, unformattedTimeFromUser) -> object:
        """
        Takes time length input from user.
        Convert input from user into integer format
        Returns a dictionary of integers corresponding
        to Hours , Minutes , Seconds , respectively
        """
        while True:
            try:
                timeUnits = self.extractDistinctTimeUnits(
                    unformattedTimeFromUser
                )
                return timeUnits
            except InvalidTimeInputError as error:
                print(error)

    def extractDistinctTimeUnits(self, inputFromUser: str) -> NamedTuple:
        stringTimeUnits = inputFromUser.split(":")
        if stringTimeUnits:
            return self.convertTimeUnitsToIntegers(stringTimeUnits)
        else:
            raise InvalidTimeInputError(stringTimeUnits)

    def convertTimeUnitsToIntegers(self, stringTimeUnits: list) -> NamedTuple:
        integerTimeUnits = list(map(int, stringTimeUnits))
        timeFromUser = RequestDetails(
            integerTimeUnits[0], integerTimeUnits[1], integerTimeUnits[2]
        )
        return timeFromUser


class TimeConverter:
    def __init__(self, timeComponents):
        self.timeComponents = timeComponents

    def getTimeComponent(self, timeUnit):
        seconds = self.getTotalSeconds()

        if timeUnit == "minutes":
            return self.__calculateTotalMinutes(seconds)
        elif timeUnit == "hours":
            return self.__calculateTotalHours(seconds)
        else:
            raise ValueError(
                "Invalid Time Component. "
                "Please request either minutes or hours"
            )

    def getTotalSeconds(self):
        totalSeconds = (self.timeComponents.hours * 3600) + \
                       (self.timeComponents.minutes * 60) + \
                       (self.timeComponents.seconds)
        return totalSeconds

    def __calculateTotalHours(self, seconds) -> int:
        secondsPerHour = 3600
        return seconds / secondsPerHour

    def __calculateTotalMinutes(self, seconds) -> int:
        secondsPerMinute = 60
        totalMinutes = seconds / secondsPerMinute
        return totalMinutes


class Date:
    def __init__(self) -> None:
        self.currentDate = pendulum.now()

    def computeDaysTillDeadline(self, userDeadline) -> int:
        daysBeforeDeadline = userDeadline.diff(self.currentDate).in_days()
        return daysBeforeDeadline

    def encodeUserDeadline(self, userDeadline: str):
        while True:
            try:
                serializedDeadline = pendulum.parse(
                    userDeadline,
                    strict=False
                )
                return serializedDeadline
            except InvalidDateFromUserError.PendulumCannotParseData:
                InvalidDateFromUserError.handleInvalidDateFromUser()


class Sessions:
    def __init__(self, minutes, minutesPerSession) -> None:
        self.minutes = minutes
        self.minutesPerSession = minutesPerSession

    def calculateSessionsPerDay(
        self, daysUntilDeadline
    ) -> float:
        totalSessions = self.calculateTotalSessions()
        dailySessions = totalSessions / daysUntilDeadline
        dailySessions = round(dailySessions, 3)
        return dailySessions

    def calculateTotalSessions(self) -> int:
        requiredSessions = self.minutes / self.minutesPerSession
        wholeRequiredSessions = math.ceil(requiredSessions)
        return wholeRequiredSessions


class DailyTimeCalculator:
    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @staticmethod
    def isWholeNumber(floatInput: float):
        integerPart = math.trunc(floatInput)
        valueIsEqualToWholeNumber = math.isclose(
            integerPart,
            floatInput,
            abs_tol=0
        )
        return valueIsEqualToWholeNumber

    def calculateHoursFromSeconds(self):
        seconds = 0
        minutes = 0
        secondsInOneHour = 3600
        if secondsInOneHour > self.seconds:
            return self.calculateMinutesFromSeconds()
        else:
            hours = self.seconds / secondsInOneHour
            if self.isWholeNumber(hours):
                dailyTime = DailyTimeCalculator(hours, minutes, seconds)
                return dailyTime
            else:
                return self._correctFloatingHours(hours, minutes, seconds)

    def _correctFloatingHours(self, hours: number, minutes: number, seconds: number):
        hoursRoundedDown = math.floor(hours)
        hoursFraction = hours - hoursRoundedDown

        minutesFromHoursFloat = hoursFraction * 60
        minutes += minutesFromHoursFloat
        dailyTime = DailyTimeCalculator(hoursRoundedDown, minutes, seconds)

        return self.normalizeMinutes(dailyTime)

    def calculateMinutesFromSeconds(self):
        secondsInOneHour   = 3600
        secondsInOneMinute = 60
        if secondsInOneHour > self.seconds > secondsInOneMinute:
            hours = 0
            minutes = self.seconds / 60
            seconds = 0
            dailyTime = DailyTimeCalculator(hours, minutes, seconds)
            if self.isWholeNumber(minutes):
                return dailyTime
            else:
                return self.normalizeMinutes(dailyTime)
        else:
            raise ValueError("This program was not created to manage time "
                             "periods less than a minute. Please supply a "
                             "more substantial amount")

    def normalizeMinutes(self, dailyTime):
        dailyTimeGenerator = self._normalizeMinutes(dailyTime)
        finalDailyTime = dailyTime

        try:
            while True:
                finalDailyTime = next(dailyTimeGenerator)
        except StopIteration:
            pass

        return self.makeTimeComponentsWholeNumbers(finalDailyTime)

    def _normalizeMinutes(self, dailyTime):
        hours = dailyTime.hours
        minutes = dailyTime.minutes
        seconds = dailyTime.seconds

        while minutes >= 60:
            hours += minutes / 60
            minutes -= 60
            if self.isWholeNumber(hours):
                dailyTimeWithWholeHour = DailyTimeCalculator(
                    hours,
                    minutes,
                    seconds
                )
                yield dailyTimeWithWholeHour
            else:
                hoursRoundedDown = math.floor(hours)
                hoursFraction = hours - hoursRoundedDown

                minutesFromHoursFloat = hoursFraction * 60
                minutes += minutesFromHoursFloat
                dailyTimeHoursUnadjustedMinutes = DailyTimeCalculator(
                    hoursRoundedDown,
                    minutes,
                    dailyTime.seconds
                )
                yield dailyTimeHoursUnadjustedMinutes

    def makeTimeComponentsWholeNumbers(self, dailyTime):
        hours = dailyTime.hours
        minutes = dailyTime.minutes
        seconds = dailyTime.seconds

        if self.isWholeNumber(minutes):
            return dailyTime
        else:
            return self._correctFloatingMinutes(hours, minutes, seconds)

    def _correctFloatingMinutes(self, hours, minutes, seconds):
        minutesRoundedDown = math.floor(minutes)
        minutesFraction = minutes - minutesRoundedDown

        secondsFromMinutesFloat = minutesFraction * 60
        seconds += secondsFromMinutesFloat
        dailyTimeFinalAdjusted = DailyTimeCalculator( hours, minutesRoundedDown, math.ceil(seconds) )
        if dailyTimeFinalAdjusted:
            return dailyTimeFinalAdjusted
        else:
            raise ValueError(
                "The final daily time adjusted is not processed properly"
            )


class PrinterInterface(ABC):
    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError(
            "You are trying to instantiate an "
            "abstract class. Please desist."
        )


class TotalSessions(PrinterInterface):
    def __init__(self, requiredSessions, minutesPerSession):
        self.requiredSessions = requiredSessions
        self.minutesPerSession = minutesPerSession

    def display(self):
        print("")
        sessions = f"[ {self.requiredSessions} ]"
        print(f"{sessions} sessions are required to complete content")
        print("")
        print("given that you wish to allocate")
        print("")
        print(f"[ {self.minutesPerSession} ] minutes per session")
        print("")


class DailySessions(PrinterInterface):
    def __init__(self, requiredDailySessions, userDeadline):
        self.requiredDailySessions = requiredDailySessions
        self.simplifiedUserDeadline = userDeadline.format("MMMM DD, YYYY")

    def display(self):
        dailySessions = f"[ {self.requiredDailySessions:.2f} ]"
        print(f"{dailySessions} daily sessions are required to complete content")
        userDeadline = f"[ {self.simplifiedUserDeadline} ]"
        print("")
        print("given that you would like to complete the content by")
        print("")
        print(f"{userDeadline}")
        print("")


class DailyTime(PrinterInterface):
    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def display(self) -> None:
        self.printDailyTimeToUser()

    def printDailyTimeToUser(self):
        if self.hours >= 1:
            self.printHoursPromptToUser()
        elif self.hours < 1:
            self.printMinutesPromptToUser()
        else:
            raise ValueError("Hours are not being processed properly.")

    def printHoursPromptToUser(self):
        print(f"Accordingly, you should spend\n\
                {self.hours} hours,\n\
                {self.minutes} minutes, and {self.seconds} seconds per day\n\
                in order to complete the content\n\
                by the deadline you have given.\n")

    def printMinutesPromptToUser(self):
        print(f"The daily number of minutes you should spend consuming the content is\n\
                {self.minutes} minutes and {self.seconds} seconds.\n")


class PrinterContext:
    def __init__(self, displayImplementation):
        self.displayImplementation = displayImplementation

    def displayDetailsToUser(self) -> None:
        for implementation in self.displayImplementation:
            implementation.display()
