import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import ttk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Datos")
        self.sidebar_visible = True

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.root.attributes('-toolwindow', True)
        self.root.geometry("1280x720")

        self.bg_color = "#272822"
        self.text_color = "#f8f8f2"
        self.button_bg = "#383830"
        self.button_text = "#f8f8f2"
        self.highlight_color = "#66d9ef"

        self.font = ('Courier New', 18)

        self.sidebar_visible = True
        self.current_view = "DATOS"
        self.graph_color = "blue"  # Color predeterminado de la gráfica

        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(fill='both', expand=True)
        self.graph_color_label = tk.Label(
            self.graph_frame, text=f"Color de la Gráfica: {self.graph_color}", font=self.font)

        self.x_label = "X"  # Etiqueta predeterminada para el eje X
        self.y_label = "Y"  # Etiqueta predeterminada para el eje Y
        # Crear un menú de edición
        self.edit_menu = tk.Menu(self.root)
        self.root.config(menu=self.edit_menu)

 # Crear un menú de edición
        self.edit_menu = tk.Menu(self.root)
        self.root.config(menu=self.edit_menu)

        # Opción para cambiar el color
        self.edit_menu.add_command(
            label="Cambiar Color de la Gráfica", command=self.change_graph_color)

        # Opción para asignar nombres a los ejes
        self.edit_menu.add_command(
            label="Asignar Nombres a los Ejes", command=self.assign_axis_labels)
        self.create_sidebar()
        self.create_data_section()
        self.create_graph_section()

        self.root.mainloop()

    def change_graph_color(self):
        # Función para cambiar el color de la gráfica
        if hasattr(self, 'data'):
            # Solicitar al usuario que seleccione un nuevo color
            # [1] para obtener el código hexadecimal del color
            new_color = colorchooser.askcolor()[1]

            if new_color:
                # Actualizar el color de la gráfica y la etiqueta de color
                self.graph_color = new_color
                self.graph_color_label.config(
                    text=f"Color de la Gráfica: {new_color}")

                # Volver a trazar la gráfica con el nuevo color
                self.plot_graph()

    def assign_axis_labels(self):
        # Función para asignar nombres a los ejes
        if hasattr(self, 'data'):
            # Solicitar al usuario que ingrese nombres para los ejes
            x_label = simpledialog.askstring(
                "Asignar Eje X", "Ingrese un nombre para el Eje X:")
            y_label = simpledialog.askstring(
                "Asignar Eje Y", "Ingrese un nombre para el Eje Y:")

            if x_label and y_label:
                # Actualizar las etiquetas de los ejes
                self.x_label = x_label
                self.y_label = y_label
                self.axis_labels_label.config(
                    text=f"Eje X: {x_label}, Eje Y: {y_label}")

                # Volver a trazar la gráfica con las nuevas etiquetas de los ejes
                self.plot_graph()

    def create_sidebar(self):
        self.sidebar_frame = tk.Frame(self.root, bg=self.bg_color, width=200)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill='y', side='left')

        self.sidebar_label = tk.Label(
            self.sidebar_frame, text="Menú", bg=self.bg_color, fg=self.text_color, font=self.font)
        self.sidebar_label.pack(pady=10)

        data_icon = Image.open("data_icon.png")
        data_icon = data_icon.resize((32, 32))
        self.data_icon = ImageTk.PhotoImage(data_icon)

        graph_icon = Image.open("graph_icon.png")
        graph_icon = graph_icon.resize((32, 32))
        self.graph_icon = ImageTk.PhotoImage(graph_icon)

        edit_icon = Image.open("edit_icon.png")
        edit_icon = edit_icon.resize((32, 32))
        self.edit_icon = ImageTk.PhotoImage(edit_icon)

        self.data_button = tk.Button(self.sidebar_frame, image=self.data_icon, text="Datos", compound="left",
                                     command=lambda: self.switch_view("DATOS"), bg=self.button_bg, fg=self.button_text, font=self.font)
        self.data_button.pack(pady=5)

        self.graph_button = tk.Button(self.sidebar_frame, image=self.graph_icon, text="Gráfica", compound="left",
                                      command=lambda: self.switch_view("GRAFICA"), bg=self.button_bg, fg=self.button_text, font=self.font)
        self.graph_button.pack(pady=5)

        self.edit_button = tk.Button(self.sidebar_frame, image=self.edit_icon, text="Editar", compound="left",
                                     command=lambda: self.switch_view("EDITAR"), bg=self.button_bg, fg=self.button_text, font=self.font)
        self.edit_button.pack(pady=5)

        self.sidebar_frame.pack_propagate(0)

    def create_data_section(self):
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill='both', expand=True)

        self.data_label = tk.Label(
            self.data_frame, text="Subir Datos", font=self.font)
        self.data_label.pack()

        self.upload_button = tk.Button(self.data_frame, text="Cargar Archivo",
                                       command=self.upload_file, bg='blue', fg='white', font=self.font)
        self.upload_button.pack()

        self.download_button = tk.Button(self.data_frame, text="Descargar Plantilla",
                                         command=self.download_template, bg='blue', fg='white', font=self.font)
        self.download_button.pack()

        self.data_display = tk.Text(
            self.data_frame, height=10, width=40, font=self.font)
        self.data_display.pack()

        self.data_table = ttk.Treeview(
            self.data_frame, columns=("X", "Y"), show="headings")
        self.data_table.heading("X", text="X")
        self.data_table.heading("Y", text="Y")
        self.data_table.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[(
            "Archivos de Datos", "*.txt *.csv")])
        if file_path:
            try:
                extension = os.path.splitext(file_path)[1].lower()
                if extension == ".csv":
                    self.data = pd.read_csv(file_path)
                elif extension == ".txt":
                    self.data = pd.read_csv(
                        file_path, delimiter=',')
                self.data_display.delete("1.0", tk.END)
                self.data_display.insert(
                    tk.END, "Datos cargados correctamente.")
                self.update_table()
            except Exception as e:
                self.data_display.delete("1.0", tk.END)
                self.data_display.insert(
                    tk.END, f"Error al cargar los datos: {str(e)}")

    def update_table(self):
        self.data_table.delete(*self.data_table.get_children())
        for index, row in self.data.iterrows():
            self.data_table.insert("", "end", values=(row['X'], row['Y']))

    def create_graph_section(self):
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(fill='both', expand=True)

        self.graph_label = tk.Label(
            self.graph_frame, text="Gráfica de Datos", font=self.font)
        self.graph_label.pack()

        self.graph_color_label = tk.Label(
            self.graph_frame, text=f"Color de la Gráfica: {self.graph_color}", font=self.font)
        self.graph_color_label.pack()

        self.axis_labels_label = tk.Label(
            self.graph_frame, text=f"Eje X: {self.x_label}, Eje Y: {self.y_label}", font=self.font)
        self.axis_labels_label.pack()

        self.graph_canvas = tk.Canvas(self.graph_frame)
        self.graph_canvas.pack()

    def load_data(self):
        if hasattr(self, 'data'):
            pass
        else:
            self.data_display.insert(
                tk.END, "\nCarga los datos primero utilizando el menú 'Abrir'.")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
        else:
            self.sidebar_frame.pack(fill='y', side='left')
        self.sidebar_visible = not self.sidebar_visible

    def switch_view(self, view):
        if view == self.current_view:
            return

        self.data_frame.pack_forget()
        self.graph_frame.pack_forget()

        if view == "DATOS":
            self.data_frame.pack(fill='both', expand=True)
        elif view == "GRAFICA":
            self.graph_frame.pack(fill='both', expand=True)
            if hasattr(self, 'data'):
                self.plot_graph()

        self.current_view = view
        if self.sidebar_visible:
            self.sidebar_frame.pack(fill='y', side='left')

    def plot_graph(self):
        if hasattr(self, 'data'):
            self.graph_canvas.delete("all")

            plt.figure(figsize=(6, 4))
            plt.plot(self.data['X'], self.data['Y'],
                     marker='o', color=self.graph_color)
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
            plt.title('Gráfica de Datos')
            plt.grid(True)

            self.plot = FigureCanvasTkAgg(plt.gcf(), master=self.graph_canvas)
            self.plot.draw()
            self.plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def download_template(self):
        template_path = "data/formato.txt"

        file_path = filedialog.asksaveasfilename(
            initialdir="/", title="Guardar como", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        if file_path:
            try:
                if not file_path.endswith(".txt"):
                    file_path += ".txt"

                with open(template_path, 'rb') as template_file:
                    template_content = template_file.read()

                with open(file_path, 'wb') as destination_file:
                    destination_file.write(template_content)

                self.data_display.delete("1.0", tk.END)
                self.data_display.insert(
                    tk.END, "Plantilla descargada correctamente.")
            except Exception as e:
                self.data_display.delete("1.0", tk.END)
                self.data_display.insert(
                    tk.END, f"Error al descargar la plantilla: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
