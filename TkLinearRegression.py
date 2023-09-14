from tkinter import *
from tkinter import messagebox
from tkinter.tix import *
from tkinter import ttk
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def updatelists():
      lstdepth.delete(0,END)
      lstpressure.delete(0,END)
      for depth in depths:
           lstdepth.insert(END,depth)
      for pressure in pressures:
           lstpressure.insert(END,pressure)

def add():
      if txtdepth.get() in depths:
         i = depths.index(txtdepth.get())
         depths[i] = txtdepth.get()
         pressures[i] = txtpressure.get()
      else:
         depths.append(txtdepth.get())
         pressures.append(txtpressure.get())
      updatelists()
      #plot()

def delete():
      try:
         d = lstdepth.get(lstdepth.curselection())
         if d in depths:
            i = depths.index(d)
            del depths[i]
            del pressures[i]
            lstdepth.delete(i)
            lstpressure.delete(i)
            lstpredpressure.delete(i)
            plot()
      except:
            pass

def plot():

      depths = list(lstdepth.get(0,lstdepth.size()-1))

      if len(depths) == 0:
         return
      
      pressures = list(lstpressure.get(0,lstpressure.size()-1))
      depths = [float(n) for n in depths]
      pressures = [float(n) for n in pressures]
      data["depths"] = depths
      data["pressures"] = pressures
      df = pd.DataFrame(data)
      X = df[["depths"]]
      y = df["pressures"]
      model = LinearRegression()
      model.fit(X,y)
      y_pred = model.predict(X)
      lstpredpressure.delete(0,END)
      for n in y_pred:
           lstpredpressure.insert(END,n)
      txtintercept.delete(0,END)
      txtintercept.insert(0,str(round(model.intercept_,2)))
      txtslope.delete(0,END)
      txtslope.insert(0,str(round(model.coef_[0],2)))
      clearplot()
      fig = plt.figure()
      ax = fig.add_subplot(111)

      fig.set_size_inches(5, 4)

      if txtxlabel.get() == "" and txtylabel.get() == "" and txttitle.get() == "" and cmbcolorinitial.get() == "" and cmbcolorprediction.get() == "" and cmbcolordotinitial.get() == "" and cmbcolordotprediction.get() == "" and txtmodifynormal.get() == "" and txtmodifyprediction.get() == "":
            ax.plot(X,y,color="red",marker="o",markerfacecolor="blue",label="Presion actual")
            ax.plot(X,y_pred,color="blue",marker="o",markerfacecolor="blue",label="Presion ajustada")
            ax.set_title("Presion vs. Profundidad")
            ax.set_xlabel("Profundidad")
            ax.set_ylabel("Presion")
            ax.legend()
      else:
            plot_modify()
      # canvas = FigureCanvasTkAgg(fig,master=window)
      # canvas.draw()
      # canvas.get_tk_widget().pack()
      plt.show()

def plot_modify():
      depths = list(lstdepth.get(0,lstdepth.size()-1))

      if len(depths) == 0:
         return
      pressures = list(lstpressure.get(0,lstpressure.size()-1))
      depths = [float(n) for n in depths]
      pressures = [float(n) for n in pressures]
      data["depths"] = depths
      data["pressures"] = pressures
      df = pd.DataFrame(data)
      X = df[["depths"]]
      y = df["pressures"]
      model = LinearRegression()
      model.fit(X,y)
      y_pred = model.predict(X)
      lstpredpressure.delete(0,END)
      for n in y_pred:
           lstpredpressure.insert(END,n)
      txtintercept.delete(0,END)
      txtintercept.insert(0,str(round(model.intercept_,2)))
      txtslope.delete(0,END)
      txtslope.insert(0,str(round(model.coef_[0],2)))
      clearplot()
      fig = plt.figure()
      ax = fig.add_subplot(111)
      fig.set_size_inches(5, 4)
      if cmbcolorinitial.get() == "":
            cmbcolorinitial.set("Rojo")
      if cmbcolorprediction.get() == "":
            cmbcolorprediction.set("Azul")
      if cmbcolordotinitial.get() == "":
            cmbcolordotinitial.set("Rojo")
      if cmbcolordotprediction.get() == "":
            cmbcolordotprediction.set("Azul")
      ax.plot(X,y,color=colors[cmbcolorinitial.get()],marker="o",markerfacecolor=colors[cmbcolordotinitial.get()],label=txtmodifynormal.get())
      ax.plot(X,y_pred,color=colors[cmbcolorprediction.get()],marker="o",markerfacecolor=colors[cmbcolordotprediction.get()],label=txtmodifyprediction.get())
      ax.set_title(txttitle.get())
      ax.set_xlabel(txtxlabel.get())
      ax.set_ylabel(txtylabel.get())
      ax.legend()

      # canvas = FigureCanvasTkAgg(fig,master=window)
      # canvas.draw()
      # canvas.get_tk_widget().pack()
      plt.show()

def clearplot():
      for widget in window.winfo_children():
           if "Canvas" in str(type(widget)):
              widget.destroy()

def listselected(event):
      if len(lstdepth.curselection()) == 0:
         return
      i = lstdepth.curselection()[0]
      txtdepth.delete(0,END)
      txtdepth.insert(END,depths[i])
      txtpressure.delete(0,END)
      txtpressure.insert(END,pressures[i])

def savedata():
      pd.DataFrame(data).to_csv("data.csv",index=False)

def opendata():
      if os.path.exists("data.csv"):
            data = pd.read_csv("data.csv")
            values = data.values
            lstdepth.delete(0,END)
            lstpressure.delete(0,END)
            depths.clear()
            pressures.clear()
            for row in values:
                  lstdepth.insert(END,row[0])
                  depths.append(str(row[0]))
                  lstpressure.insert(END,row[1])
                  pressures.append(str(row[1]))
      else:
            messagebox.showerror("Error","No data found to load")



depths = []
pressures = []
data = {}
window = Tk()
window.resizable(False, False)
window.geometry("790x460+100+50")


window.config(bg="white")
window.title("Regresion Lineal Simple de Presión vs. Profundidad")
#window.state("zoomed")
#window.attributes("-toolwindow", 1)

window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())

tip = Balloon(window)

color = "#43aa8b"

frame_input = Frame(window, padx=3, bg=color)
frame_input.place(x=10, y=10)

lbl_datos = Label(frame_input, text="DATOS", font=("Arial", 12, "bold"), fg="white", bg=color)
lbl_datos.grid(row=0, column=0, columnspan=2, sticky="w")

lbldepth = Label(frame_input, text="Profundidad h (m): ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lbldepth.grid(row=1, column=0, sticky="w")
txtdepth = Entry(frame_input)
txtdepth.grid(row=2, column=0)

lblpressure = Label(frame_input, text="Presión P (Pa): ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblpressure.grid(row=1, column=1, sticky="w")
txtpressure = Entry(frame_input)
txtpressure.grid(row=2, column=1)

lbl_indicacion = Label(frame_input, text="Los decimales se separan con punto", anchor="w", font=("Arial", 8, "italic", "bold"), fg="white", bg=color)
lbl_indicacion.grid(row=3, column=0, sticky="w")

frame_buttons = Frame(window, bg="white", padx=40,)
frame_buttons.place(x=10, y=100)

btnadd = Button(frame_buttons, text="AGREGAR", command=add, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa")
btnadd.grid(row=0, column=0, sticky="nsew")

btndelete = Button(frame_buttons, text="BORRAR", command=delete, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa")
btndelete.grid(row=0, column=1, sticky="nsew")

btnplot = Button(frame_buttons, text="GRAFICAR", command=plot, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa")
btnplot.grid(row=1, column=1, sticky="nsew")

btnsave = Button(frame_buttons, text="GUARDAR DATOS", command=savedata, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa")
btnsave.grid(row=2, column=0, sticky="nsew")

btnopen = Button(frame_buttons, text="CARGAR DATOS", command=opendata, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa")
btnopen.grid(row=1, column=0, sticky="nsew")

frame_lists = Frame(window, bg=color, pady=82)
frame_lists.place(x=350, y=10)

lbl_tabla = Label(frame_lists, text="TABLA", font=("Arial", 12, "bold"), fg="white", bg=color)
lbl_tabla.grid(row=0, column=0, columnspan=3, sticky="nsew")

lblintercept = Label(frame_lists, text="Profundidad", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblintercept.grid(row=1, column=0)

lblintercept = Label(frame_lists, text="Presión", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblintercept.grid(row=1, column=1)

lblintercept = Label(frame_lists, text="Presión ajustada", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblintercept.grid(row=1, column=2)

lstdepth = Listbox(frame_lists)
lstdepth.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

lstpressure = Listbox(frame_lists)
lstpressure.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

lstpredpressure = Listbox(frame_lists)
lstpredpressure.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

lblintercept = Label(frame_lists, text="Y-Intercepción: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblintercept.grid(row=3, column=0)

txtintercept = Entry(frame_lists)
txtintercept.grid(row=4, column=0)

lblslope = Label(frame_lists, text="Pendiente: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblslope.grid(row=3, column=1)

txtslope = Entry(frame_lists)
txtslope.grid(row=4, column=1)

lstdepth.bind("<<ListboxSelect>>", listselected)

tip.bind_widget(lstdepth, balloonmsg="Profundidad")
tip.bind_widget(lstpressure, balloonmsg="Presión")
tip.bind_widget(lstpredpressure, balloonmsg="Presión ajustada")

frame_modifiers = Frame(window, bg=color,)

frame_modifiers.place(x=10, y=195)
lbl_modificar_tabla = Label(frame_modifiers, text="MODIFICAR TABLA", font=("Arial", 12, "bold"), fg="white", bg=color)
lbl_modificar_tabla.grid(row=0, column=0, columnspan=2, sticky="w")

lblxlabel = Label(frame_modifiers, text="Eje X: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblxlabel.grid(row=1, column=0, sticky="w")

txtxlabel = Entry(frame_modifiers)
txtxlabel.grid(row=1, column=1)

lblylabel = Label(frame_modifiers, text="Eje Y: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblylabel.grid(row=2, column=0, sticky="w")

txtylabel = Entry(frame_modifiers)
txtylabel.grid(row=2, column=1)

lbltitle = Label(frame_modifiers, text="Titulo: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lbltitle.grid(row=3, column=0, sticky="w")

txttitle = Entry(frame_modifiers)
txttitle.grid(row=3, column=1)

colors = {
      "Rojo": "red",
      "Azul": "blue",
      "Verde": "green",
      "Amarillo": "yellow",
      "Negro": "black",
      "Blanco": "white",
      "Naranja": "orange",
      "Morado": "purple",
      "Rosa": "pink",
      "Marrón": "brown"
}

lblcolorinitial = Label(frame_modifiers, text="Color de la gráfica original: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblcolorinitial.grid(row=4, column=0,sticky="w")

cmbcolorinitial = ttk.Combobox(frame_modifiers, width=17, state="readonly")
cmbcolorinitial["values"] = list(colors.keys())
cmbcolorinitial.grid(row=4, column=1, sticky="w")

lblcolorprediction = Label(frame_modifiers, text="Color de la gráfica ajustada: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblcolorprediction.grid(row=5, column=0, sticky="w")

cmbcolorprediction = ttk.Combobox(frame_modifiers, width=17, state="readonly")
cmbcolorprediction["values"] = list(colors.keys())
cmbcolorprediction.grid(row=5, column=1,sticky="w")

lblcolordotinitial = Label(frame_modifiers, text="Color de puntos - gráfica original: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblcolordotinitial.grid(row=6, column=0,sticky="w")

cmbcolordotinitial = ttk.Combobox(frame_modifiers, width=17, state="readonly")
cmbcolordotinitial["values"] = list(colors.keys())
cmbcolordotinitial.grid(row=6, column=1,sticky="w")

lblcolordotprediction = Label(frame_modifiers, text="Color de puntos - gráfica ajustada: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblcolordotprediction.grid(row=7, column=0,sticky="w")

cmbcolordotprediction = ttk.Combobox(frame_modifiers, width=17, state="readonly")
cmbcolordotprediction["values"] = list(colors.keys())
cmbcolordotprediction.grid(row=7, column=1,sticky="w")

lblmodifynormal = Label(frame_modifiers, text="Nombre gráfica 1: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblmodifynormal.grid(row=8, column=0,sticky="w")

txtmodifynormal = Entry(frame_modifiers)
txtmodifynormal.grid(row=8, column=1,sticky="w")

lblmodifyprediction = Label(frame_modifiers, text="Nombre gráfica 2: ", anchor="w", font=("Arial", 10), fg="white", bg=color)
lblmodifyprediction.grid(row=9, column=0,sticky="w")

txtmodifyprediction = Entry(frame_modifiers)
txtmodifyprediction.grid(row=9, column=1,sticky="w")

btnapply = Button(frame_modifiers, text="APLICAR", command=plot_modify, font=("Arial", 10, "bold"), fg="black", bg="#f8f9fa",)
btnapply.grid(row=10, column=1,sticky="w")

window.mainloop()