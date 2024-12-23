def getTimeInputFromUser() -> str:
    prompt = (
        "What is the total amount of time\n"
        "concerning the video content you would like to complete: "
    )
    print("")
    unformattedTimeFromUser = input(prompt)
    return unformattedTimeFromUser


def askMinutesPerSession() -> int:
    while True:
        try:
            print("")
            numberMinutes = input("How many minutes per session? ")
            return int(numberMinutes)
        except InvalidSessionMinutesError as error:
            error.handleInvalidSessionMinutes()


def askDeadlineFromUser() -> str:
    print("")
    deadlineFromUser = input(
            "By what date would you like to complete the content: "
    )
    return deadlineFromUser
