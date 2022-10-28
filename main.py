import tkinter as tk

TEXT = "Je me suis rendu compte peu à peu de ce que fut jusqu'à présent toute grande philosophie : la confession de son " \
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

TEXT.replace(" – ", " ")
split_text = [TEXT[idx:idx + 60] for idx in range(0, len(TEXT), 60)]
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
    global focus_index
    shift_keys = {"Shift_L", "Shift_R"}
    if event.keysym not in shift_keys:
        index = int(texts_down[focus_index].index(tk.INSERT).split(".")[1]) - 1
        print(index)
        try:
            if event.char == texts_up[focus_index].get(texts_up[focus_index].index(f"1.{index}")):
                texts_up[focus_index].tag_add("correct", texts_up[focus_index].index(f"1.{index}"))
            else:
                texts_up[focus_index].tag_add("wrong", texts_up[0].index(f"1.{index}"))
        except tk.TclError:
            pass
        if index + 2 == len(texts_up[focus_index].get("1.0", "end")):
            focus_index += 1
            texts_down[focus_index].focus()


def do_backspace(event):
    shift_keys = {"Shift_L", "Shift_R"}
    if event.keysym not in shift_keys:
        try:
            index = int(texts_down[focus_index].index(tk.INSERT).split(".")[1])
            texts_up[focus_index].tag_remove("wrong", texts_up[focus_index].index(f"1.{index}"))
            texts_up[focus_index].tag_remove("correct", texts_up[focus_index].index(f"1.{index}"))
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

rely = 0.4
texts_up = []
texts_down = []
for line in split_text:
    current_index = split_text.index(line)
    texts_up.append(tk.Text(width=50, height=1, pady=2,  relief="flat", font=("Arial", 14, "normal")))
    texts_up[current_index].insert(f"{current_index}.0", line)
    texts_up[current_index].config(state="disabled")
    rely += 0.2
    texts_up[current_index].place(relx=0.5, rely=rely, anchor="s")
    texts_up[current_index].tag_configure("correct", foreground="green")
    texts_up[current_index].tag_configure("wrong", foreground="red")

    texts_down.append(tk.Text(width=50, height=1, font=("Arial", 14, "normal")))
    texts_down[current_index].place(relx=0.5, rely=rely, anchor="n")

focus_index = 0
texts_down[focus_index].focus()

win.mainloop()
