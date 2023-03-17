from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from graph import Graph


class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.filepath = None
        self.graph = None

        self.state("zoomed")

        Label(self, fg='black', font=('Arial', 16), justify="center", text="Graph Theory project").pack(pady=10)
        self.content = Frame(self)
        self.content.place(relx=.5, rely=.5, anchor=CENTER)
        self.table_frame = Frame(self.content)
        self.table_frame.pack(pady=10)
        Label(self.table_frame, fg='black', font=('Arial', 16), justify="center", text="No graph selected").pack()
        self.analyze_frame = Frame(self.content)
        self.analyze_frame.pack(pady=10)
        self.button_frame = Frame(self.content)
        self.button_frame.pack()
        Button(self.button_frame, text='Load graph', command=self.load_graph).grid(row=0, column=0, padx=10)
        Button(self.button_frame, text='Analyze graph', command=self.analyze_graph).grid(row=0, column=1, padx=10)

    def load_graph(self):
        self.filepath = askopenfilename(filetypes=[("text files", "*.txt")], initialdir="./test files/")
        if self.filepath is None or self.filepath == "":
            showinfo("Warning", "No file selected !")
        else:
            self.graph = Graph(self.filepath)
            self.add_graph_table()

    def add_graph_table(self):
        for child in self.table_frame.winfo_children():
            child.destroy()
        matrix = self.graph.as_matrix()
        sizes = [max(map(len, col)) + 3 for col in zip(*matrix)]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != "*":
                    color = 'blue'
                else:
                    color = 'black'
                Label(self.table_frame, width=sizes[j], fg=color, font=('Arial', 12), justify="center", text=matrix[i][j], relief=RAISED).grid(row=i, column=j)

    def analyze_graph(self):
        if self.graph is None:
            showinfo("Warning", "No Graph selected! Select a graph to be able to analyze it.")
        else:
            for child in self.analyze_frame.winfo_children():
                child.destroy()
            matrix = [["vertex"] + [vertex.name for vertex in self.graph.vertices]]
            print(matrix)
            matrix += [["rank"] + [str(rank) for rank in self.graph.get_rank()]]
            matrix += [["earliest date"] + [str(date) for date in self.graph.get_earliest_date()]]
            matrix += [["latest date"] + [str(date) for date in self.graph.get_latest_date()]]
            matrix += [["total float"] + [str(Float) for Float in self.graph.get_total_float()]]
            matrix += [["free float"] + [str(Float) for Float in self.graph.get_free_float()]]
            sizes = [max(map(len, col)) + 2 for col in zip(*matrix)]
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    Label(self.analyze_frame, width=sizes[j], fg='blue', font=('Arial', 12), justify="center", text=matrix[i][j], relief=RAISED).grid(row=i, column=j)
