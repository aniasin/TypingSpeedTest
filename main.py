import tkinter as tk

TIME_TEST = 300

count = TIME_TEST
timer = ""


def start(time_left):
    global timer
    global count
    if count > 0:
        check_typing()
        count -= .5
        timer = win.after(500, start, count)
    else:
        win.after_cancel(timer)
        game_end()


def check_typing():
    if count < TIME_TEST:
        current_time = TIME_TEST - count


def game_end():
    pass


def key_press(event):
    shift_keys = {"Shift_L", "Shift_R"}
    if event.keysym not in shift_keys:
        try:
            index = int(text_down.index(tk.INSERT).split(".")[1]) - 1
            if event.char == text_up.get(text_up.index(f"1.{index}")):
                text_up.tag_add("correct", text_up.index(f"1.{index}"))
            else:
                text_up.tag_add("wrong", text_up.index(f"1.{index}"))
        except tk.TclError:
            pass


def do_backspace(event):
    shift_keys = {"Shift_L", "Shift_R"}
    if event.keysym not in shift_keys:
        try:
            index = int(text_down.index(tk.INSERT).split(".")[1])
            text_up.tag_remove("wrong", text_up.index(f"1.{index}"))
            text_up.tag_remove("correct", text_up.index(f"1.{index}"))
        except tk.TclError:
            pass


win = tk.Tk()
win.title("Typing Test")
win.config(width=700, height=400, bg="white")

win.bind("<Key>", key_press)
win.bind("<BackSpace>", do_backspace)

label_title = tk.Label(text="Typing Speed Test", font=("Arial", 20, "bold"), bg="white", fg="black")
label_title.place(relx=0.5, rely=0, anchor="n")

label_result = tk.Label(text="words/minutes", font=("Arial", 18, "normal"), bg="white", fg="green")
label_result.place(relx=0.5, rely=0.1, anchor="n")

label_precision = tk.Label(text="Precision: ", font=("Arial", 18, "normal"), bg="white", fg="green")
label_precision.place(relx=0.5, rely=0.2, anchor="n")

text_up = tk.Text(width=50, height=1, pady=2,  relief="flat", font=("Arial", 14, "normal"))
text_up.insert('1.0', 'Here is my text to insert')
text_up.config(state="disabled")
text_up.place(relx=0.5, rely=0.5, anchor="s")
text_up.tag_configure("correct", foreground="green")
text_up.tag_configure("wrong", foreground="red")

text_down = tk.Text(width=50, height=1, font=("Arial", 14, "normal"))
text_down.place(relx=0.5, rely=0.5, anchor="n")
text_down.focus()

win.mainloop()
