from tkinter import Tk,Label,StringVar,Entry,Button,Canvas,messagebox, Frame
from random import randint

def cancel():
    global job
    if job is not None:
        mw.after_cancel(job)
        job = None

def goodbye_world():
    print ("Stopping Feed")
    cancel()

def hello_world():
    print ("Starting Feed")
    print_sleep()

def print_sleep():
    global job
    foo = randint(2000,4500)
    # print ("Sleeping", 10)
    # print(job)
    job = mw.after(100, print_sleep)

mw = Tk()
job = None
btn_hello = Button(mw, text = 'hello', command = hello_world)
btn_gb = Button(mw, text = 'good bye', command = goodbye_world)
mw.bind('<Key>', lambda x : print(x.keysym))
mw.bind('<Button>', lambda x : print('Mouse', x.num))
btn_hello.pack()
btn_gb.pack()

mw.mainloop()