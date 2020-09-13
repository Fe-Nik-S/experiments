
import os
import datetime
from tkinter import Tk, IntVar, Label, Button, messagebox
from pyautogui import screenshot


PAUSE_TIME = 1000
DIR_FROM_SCREENSHOTS = os.getcwd()
DATE_FORMAT = "%Y-%m-%d_%X"


def main():
    def take_screenshot_handler():
        time_left = time_counter.get()
        if time_left > 0:
            time_counter.set(time_left - 1)
            form.after(PAUSE_TIME, take_screenshot_handler)
            return

        now = datetime.datetime.now().strftime(DATE_FORMAT)
        path_to_scr = os.path.join(DIR_FROM_SCREENSHOTS, "screen-{}.png".format(now))
        screenshot().save(path_to_scr)
        messagebox.showinfo("Screenshot", "Screenshot saved to {}".format(path_to_scr))
        time_counter.set(3)

    form = Tk()
    time_counter = IntVar()
    time_counter.set(3)

    Label(form, textvariable=time_counter, fg="red").pack()
    Button(form, text="Take screenshot after 3 secs", command=take_screenshot_handler).pack()

    form.mainloop()


if __name__ == "__main__":
    main()
