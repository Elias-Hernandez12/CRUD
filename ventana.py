from tkinter import *
from tkinter import ttk

class Ventana(Frame):
    
    def __init__(self, master=None):
        super().__init__(master, width=680, height=260)
        self.master = master
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0, width=93, height=259)
        
        self.btnNuevo = Button(frame1, text='Nuevo', command=self.fNuevo, bg='blue', fg='white')
        self.btnNuevo.place(x=5, y=50 , width=80, height= 30)
        
        self.btnModificar = Button(frame1, text='Modificar', command=self.fmodificar, bg='blue', fg='white')
        self.btnModificar.place(x=5, y=90 , width=80, height= 30)
        
        self.btnEliminar = Button(frame1, text='Eliminar', command=self.feliminar, bg='blue', fg='white')
        self.btnEliminar.place(x=5, y=130 , width=80, height= 30)
    
        frame2 = Frame(self, bg="#d3dde3")
        frame2.place(x=95, y=0, width=150, height=259)
        
        lbl1 = Label(frame2, text="ISO3: ")
        lbl1.place(x=3, y=5)
        
        self.txtISO3 = Entry(frame2)
        self.txtISO3.place(x=3, y=25, width=50, height=20)
        
        lbl2 = Label(frame2, text="PAÍS: ")
        lbl2.place(x=3, y=55)
        
        self.txtPais = Entry(frame2)
        self.txtPais.place(x=3, y=75, width=100, height=20)
        
        lbl3 = Label(frame2, text="CAPITAL: ")
        lbl3.place(x=3, y=105)
        
        self.txtCapital = Entry(frame2)
        self.txtCapital.place(x=3, y=125, width=100, height=20)

        lbl4 = Label(frame2, text="MONEDA: ")
        lbl4.place(x=3, y=155)
        
        self.txtMoneda = Entry(frame2)
        self.txtMoneda.place(x=3, y=175, width=100, height=20)
        
        self.btnGuardar = Button(frame2, text='Guardar', command=self.fguardar, bg='green', fg='white')
        self.btnGuardar.place(x=10, y=210 , width=60, height= 30)
        
        self.btnCancelar = Button(frame2, text='Cancelar', command=self.fcancelar, bg='red', fg='white')
        self.btnCancelar.place(x=80, y=210 , width=60, height= 30)
        
        self.grid = ttk.Treeview(self, column=("col1","col2","col3","col4"))
        self.grid.column("#0", width=50)
        self.grid.column("col1", width = 60, anchor = CENTER)
        self.grid.column("col2", width = 90, anchor = CENTER)
        self.grid.column("col3", width = 90, anchor = CENTER)
        self.grid.column("col4", width = 90, anchor = CENTER)
        
        self.grid.heading("#0", text = "Id", anchor = CENTER)
        self.grid.heading("col1", text = "ISO3", anchor = CENTER)
        self.grid.heading("col2", text = "PAIS", anchor = CENTER)
        self.grid.heading("col3", text = "CAPITAL", anchor = CENTER)
        self.grid.heading("col4", text = "MONEDA", anchor = CENTER)
        
        self.grid.place(x = 247, y = 0, width = 430, height = 259)
        self.grid.insert("", END, text="1", values=("ARG", "Argentina", "Buenos Aires", "ARS"))
        
    def fNuevo(self):
        pass
    
    def fmodificar(self):
        pass
    
    def feliminar(self):
        pass
    
    def fguardar(self):
        pass
    
    def fcancelar(self):
        pass