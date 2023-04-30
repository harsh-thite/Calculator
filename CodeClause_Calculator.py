import tkinter as tk
from functools import partial
import math
import re

normalcalc = True

window = tk.Tk()
window.title("Calculator")
window.geometry("300x400")
window.minsize(300, 400)

def button_click(expression, button):
    if button == "C":
        expression.set("")
    elif button == "CE":
        expression.set(expression.get()[:-1])
    elif button == "√x":
        expression.set(str(math.sqrt(eval(expression.get()))))
    elif button == "x^2":
        expression.set(str(eval(expression.get()) ** 2))
    elif button == "1/x":
        expression.set(str(1 / eval(expression.get())))
    elif button == "±":
        if expression.get()[0] == "-":
            expression.set(expression.get()[1:])
        else:
            expression.set("-" + expression.get())
    elif button == "sin":
        expression.set(str(math.sin(math.radians(float(expression.get())))))
    elif button == "cos":
        expression.set(str(math.cos(math.radians((float(expression.get()))))))
    elif button == "tan":
        expression.set(str(math.tan(math.radians((float(expression.get()))))))
    elif button == "sec":
        expression.set(str(1 / math.cos(math.radians((float(expression.get()))))))
    elif button == "csc":
        expression.set(str(1 / math.sin(math.radians((float(expression.get()))))))
    elif button == "cot":
        expression.set(str(1 / math.tan(math.radians((float(expression.get()))))))
    elif button == "x^3":
        expression.set((float(expression.get()) ** 3))
    elif button == "e^x":
        expression.set(str(math.exp(float(expression.get()))))
    elif button == "log":
        expression.set(str(math.log10(float(expression.get()))))
    elif button == "ln":
        expression.set(str(math.log(float(expression.get()))))
    elif button == "π":
        expression.set(str(math.pi))
    elif button == "!":
        expression.set(str(math.factorial(float(expression.get()))))
    elif button == "e":
        expression.set(str(math.e))
    elif button == "10^x":
        expression.set(str(10 ** float(expression.get())))
    elif button == "=" :
        express = expression.get()
        express = re.sub(r"\b0+(\d)", r"\1", express)
        try:
            expression.set(str(eval(express)))
        except:
            expression.set("Error")
    else:
        expression.set(expression.get() + str(button))

    if len(expression.get()) > 15:
        display.config(font=('Arial', 15))
    else:
        display.config(font=('Arial', 25))

    display.icursor(tk.END)



def on_key_press(event):
    if len(expression.get()) > 15:
        display.config(font=('Arial', 15))
    else:
        display.config(font=('Arial', 25))

def on_resize(event):
    width = event.width
    if len(expression.get()) > 15 and width <= 300:
        display.config(font=('Arial', 15))
    else:
        display.config(font=('Arial', 25))

window.bind("<Configure>", on_resize)  


def validate_input(key):
    allowed_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-', '*', '/']
    if key in allowed_keys:
        return True
    elif key == '\b':
        return True
    else:
        return False

expression = tk.StringVar()
expression.set("")

display = tk.Entry(window, textvariable=expression, font=('Arial', 25), justify="right", validate="key", validatecommand=(window.register(validate_input), '%S'))
display.pack(fill=tk.BOTH, expand=True)
display.bind('<Key>', on_key_press)

buttonFrame = tk.Frame(window, bg="#F7F5E3")
buttonFrame.pack(fill=tk.BOTH, expand=True)

scFrame = tk.Frame(window, bg="#F7F5E3")

buttons = ["1/x", "x^2", "√x", "/",
    "7", "8", "9", "*",
    "4", "5", "6", "-",
    "1", "2", "3", "+", 
    "0", ".", "±", "=",
    "C", "%", "<-"
]

scbutton = ["sin", "cos", "tan", "sec", "csc", "cot", "x^3", "e^x", "log", "ln", "π", "!", "(", ")", "e", "10^x"]

def on_enter(e):
    e.widget['bg'] = '#E2DFC5'

def on_leave(e):
    e.widget['bg'] = 'white'

def create_buttons(frame, buttons, mode):
    row, col = 0, 0
    for button in buttons:
        command = partial(mode, expression, button)
        btn = tk.Button(frame, text=button, font=('Arial', 16), width=5, height=0, relief='ridge', bg="white", borderwidth=0, highlightthickness=0, command=command)
        btn.grid(row=row, column=col, padx=1, pady=1, sticky=tk.NSEW)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        if button.isdigit():
            btn.bind("<Key-{}>".format(button), lambda event: mode(expression, button))

        display.bind("<Return>", lambda event: mode(expression, "="))
        display.focus_set()
        
        col += 1
        if col > 3:
            col = 0
            row += 1
    
create_buttons(buttonFrame, buttons, button_click)

def sc_click():
    global normalcalc
    if normalcalc:
        print("sc")
        buttonFrame.pack_forget()
        create_buttons(scFrame, scbutton, button_click)
        scFrame.pack(fill=tk.BOTH, expand=True)
        buttonFrame.pack(fill=tk.BOTH, expand=True)
        create_buttons(buttonFrame, buttons, button_click)
        normalcalc = False
    else:
        scFrame.pack_forget()
        buttonFrame.pack(fill=tk.BOTH, expand=True)
        create_buttons(buttonFrame, buttons, button_click)
        normalcalc = True

for i in range(6):
    buttonFrame.rowconfigure(i, weight=1)
for i in range(5):
    scFrame.rowconfigure(i, weight=1)

for i in range(4):
    scFrame.columnconfigure(i, weight=1)
    buttonFrame.columnconfigure(i, weight=1)


menubar = tk.Menu(window, font=('Arial', 55))
mode = tk.Menu(menubar, tearoff=0)
mode.add_checkbutton(label="Scientific", command=sc_click)
menubar.add_cascade(label="Standard", menu=mode)
window.config(menu=menubar)


window.mainloop()