import tkinter as tk
from textwrap import wrap

TEXT_ = "Je me suis rendu compte peu à peu de ce que fut jusqu'à présent toute grande philosophie : la confession de son " \
       "auteur, une sorte de mémoires involontaires et insensibles ; et je me suis aperçu aussi que les intentions " \
       "morales ou immorales formaient, dans toute philosophie, le véritable germe vital d'où chaque fois la plante " \
       "entière est éclose. On ferait bien en effet (et ce serait même raisonnable) de se demander, pour l'élucidation " \
       "de ce problème : comment se sont formées les affirmations métaphysiques les plus lointaines d'un philosophe ? " \
       "– on ferait bien, dis-je, de se demander à quelle morale veut-on en venir ? Par conséquent, je ne crois pas " \
       "que l' « instinct de la connaissance » soit le pire de la philosophie, mais plutôt qu'un autre instinct s'est " \
       "servi seulement, là comme ailleurs, de la connaissance (et de la méconnaissance) ainsi que d'un instrument. " \
       "Mais quiconque examinera les instincts fondamentaux de l'homme, en vue de savoir jusqu'à quel point ils ont " \
       "joué, ici surtout, leur jeu de génies inspirateurs (démons et lutins peut-être – ), reconnaîtra que ces " \
       "instincts ont tous déjà fait de la philosophie – et que le plus grand désir de chacun serait de se représenter " \
       "comme fin dernière de l'existence, ayant qualité pour dominer les autres instincts. Car tout instinct est avide " \
       "de domination : et comme tel il aspire à philosopher. Certes, chez les savants, les véritables hommes " \
       "scientifiques, il se peut qu'il en soit autrement – que ceux-ci soient, si l'on veut, en « meilleure » " \
       "posture. Peut-être y a-t-il là véritablement quelque chose comme l'instinct de connaissance, un petit rouage " \
       "indépendant qui, bien remonté, se met à travailler bravement, sans que tous les autres instincts du savant y " \
       "soient essentiellement intéressés. C'est pourquoi les véritables « intérêts » du savant se trouvent généralement" \
       "tout à fait ailleurs, par exemple dans la famille, dans l'âpreté au gain, ou dans la politique ; il est même " \
       "presque indifférent que sa petite machine soit placée à tel ou tel point de la science, et que le jeune " \
       "travailleur d' « avenir » devienne bon philologue, ou peut-être connaisseur de champignons, ou encore chimiste :" \
       "peu importe, pour le distinguer, qu'il devienne ceci ou cela. Au contraire, chez le philosophe, il n'y a rien " \
       "d'impersonnel ; et particulièrement sa morale témoigne, d'une façon décisive et absolue, de ce qu'il est, " \
       "c'est-à-dire dans quel rapport se trouvent les instincts les plus intimes de sa nature."


TEXT = TEXT_.replace(" – ", " ")
TEXT = TEXT.replace("«", '"')
TEXT = TEXT.replace("»", '"')
split_text = wrap(TEXT, 60)
TIME_TEST = 300

cursor_pos = 0
line_pos = 0
count = TIME_TEST
timer = ""


def start(time_left):
    global timer
    global count
    if count > 0:
        check_typing()
        count -= .5
        timer = win.after(1000, start, count)
    else:
        win.after_cancel(timer)
        test_end()


def check_typing():
    if count < TIME_TEST:
        current_time = TIME_TEST - count
        current_words_count = 0
        text_up = []
        text_down = []
        for text in texts_down[:line_pos + 1]:
            if cursor_pos < len(text.get("1.0", "end")):
                current_words_count += len(text.get("1.0", f"1.{cursor_pos + 1}").split())
                text_down += (text.get("1.0", f"1.{cursor_pos + 1}").split())
            else:
                current_words_count += len(text.get("1.0", "end").split())
                text_down += (text.get("1.0", "end").split())
        words_min = current_words_count / current_time
        words_min = "{:.2f}".format(words_min * 60)
        label_result.configure(text=f"{words_min} words/minutes")
        for text in texts_up[:line_pos + 1]:
            if cursor_pos < len(text.get("1.0", "end")):
                text_up += (text.get("1.0", f"1.{cursor_pos + 1}").split())
            else:
                text_up += (text.get("1.0", "end").split())
        wrong_words = len(set(text_up) - set(text_down))
        print(set(text_up) - set(text_down))
        if len(text_up) > 0:
            precision = "{:.2f}".format(((len(text_up) - wrong_words) / len(text_up)) * 100)
            label_precision.configure(text=f"Precision: {precision}%")


def test_end():
    print("Test ended!")


def key_press(event):
    global line_pos
    global cursor_pos
    shift_keys = {"Shift_L", "Shift_R", "^"}
    if event.keysym not in shift_keys:
        cursor_pos = int(texts_down[line_pos].index(tk.INSERT).split(".")[1]) - 1
        print(cursor_pos)
        print(line_pos)
        try:
            if event.char == texts_up[line_pos].get(texts_up[line_pos].index(f"1.{cursor_pos}")):
                texts_up[line_pos].tag_add("correct", texts_up[line_pos].index(f"1.{cursor_pos}"))
            else:
                texts_up[line_pos].tag_add("wrong", texts_up[0].index(f"1.{cursor_pos}"))
        except tk.TclError:
            pass
        if cursor_pos + 2 == len(texts_up[line_pos].get("1.0", "end")):
            line_pos += 1
            for text_box in texts_up:
                text_box.place(y=text_box.winfo_y() - 80)
            for text_box in texts_down:
                text_box.place(y=text_box.winfo_y() - 80)
            texts_down[line_pos].focus()


def do_backspace(event):
    global line_pos
    global cursor_pos
    shift_keys = {"Shift_L", "Shift_R"}
    if event.keysym not in shift_keys:
        try:
            cursor_pos = int(texts_down[line_pos].index(tk.INSERT).split(".")[1])
            if cursor_pos == 0:
                return
            if cursor_pos == 0:
                line_pos -= 1
                for text_box in texts_up:
                    text_box.place(y=text_box.winfo_y() + 80)
                for text_box in texts_down:
                    text_box.place(y=text_box.winfo_y() + 80)
                cursor_pos = int(texts_down[line_pos].index(tk.INSERT).split(".")[1]) - 1
                texts_down[line_pos].focus()
                texts_down[line_pos].delete("end-2c")
            texts_up[line_pos].tag_remove("wrong", texts_up[line_pos].index(f"1.{cursor_pos}"))
            texts_up[line_pos].tag_remove("correct", texts_up[line_pos].index(f"1.{cursor_pos}"))
        except tk.TclError:
            pass


win = tk.Tk()
win.title("Typing Test")
win.config(width=900, height=200, bg="white")

win.bind("<Key>", key_press)
win.bind("<BackSpace>", do_backspace)

label_title = tk.Label(text="Typing Speed Test", font=("Arial", 20, "bold"), bg="white", fg="black")
label_title.place(x=130, y=20, anchor="n")

label_result = tk.Label(text="words/minutes", font=("Arial", 18, "normal"), bg="white", fg="green")
label_result.place(x=120, y=60, anchor="n")

label_precision = tk.Label(text="Precision: ", font=("Arial", 18, "normal"), bg="white", fg="green")
label_precision.place(x=120, y=100, anchor="n")

pos_x = 280
pos_y = 20
texts_up = []
texts_down = []
for line in split_text:
    current_index = split_text.index(line)
    line += " "
    texts_up.append(tk.Text(width=50, height=1, pady=2,  relief="flat", fg="grey", font=("Arial", 14, "normal")))
    texts_up[current_index].insert(f"{current_index}.0", line)
    texts_up[current_index].config(state="disabled")
    texts_up[current_index].place(x=pos_x, y=pos_y)
    texts_up[current_index].tag_configure("correct", foreground="green")
    texts_up[current_index].tag_configure("wrong", foreground="red")
    pos_y += 40
    texts_down.append(tk.Text(width=50, height=1, font=("Arial", 14, "normal")))
    texts_down[current_index].place(x=pos_x, y=pos_y)
    pos_y += 40

texts_down[line_pos].focus()

start(TIME_TEST)
win.mainloop()
