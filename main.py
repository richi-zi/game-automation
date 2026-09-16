import time
import pyautogui

StartPic = "pic/start.png"
BattlePic = "pic/battle.png"
EndPic = "pic/end.png"


con = 0.8
waitTime = 30
baltTime = 180
checkInt = 0.5

StartCli = (959, 870)
EndCli = (964, 963)
Card = (817, 945)
Drop = (854, 788)


def click(pos):
    pyautogui.moveTo(pos, duration=0.05)
    pyautogui.mouseDown()
    time.sleep(0.15)
    pyautogui.mouseUp()


def findImg(pic):
    try:
        return pyautogui.locateOnScreen(pic, confidence=con)
    except pyautogui.ImageNotFoundException:
        return None


def waitImg(pic):
    deadline = time.monotonic() + waitTime
    while time.monotonic() < deadline:
        if findImg(pic) is not None:
            return True
        time.sleep(checkInt)
    return False


def begin():
    if waitImg(StartPic):
        click(StartCli)
        time.sleep(1)
        return "loading"
    print("begin timed out")
    return "end"


def loading():
    if waitImg(BattlePic):
        return "battle"
    print("loading timed out")
    return "end"


def battle():
    kingMiss = 0
    deadline = time.monotonic() + baltTime
    while time.monotonic() < deadline:
        click(Card)
        time.sleep(3)
        click(Drop)
        time.sleep(3)

        if findImg(BattlePic) is not None:
            kingMiss = 0
        else:
            kingMiss += 1
        if kingMiss >= 3:
            print("king miss")
            return "end"
        if findImg(EndPic) is not None:
            return "end"
        time.sleep(checkInt)
    print("battle timed out")
    return "end"


def end():
    if waitImg(EndPic):
        click(EndCli)
        time.sleep(2)
        return "begin"
    print("end timed out")
    return "detectAll"


def detectAll():
    #if no detect, force end to prevent getting stuck.
    if findImg(StartPic) is not None:
        return "begin"
    if findImg(BattlePic) is not None:
        return "battle"
    if findImg(EndPic) is not None:
        print("end detected")
    else:
        print("no state detected")
    click(EndCli)
    time.sleep(2)
    return "begin"


def main():
    time.sleep(3)
    handlers = {
        "begin": begin,
        "loading": loading,
        "battle": battle,
        "end": end,
        "detectAll": detectAll,
    }
    state = "begin"
    while True:
        print(f"state: {state}")
        state = handlers[state]()


if __name__ == "__main__":
    main()
