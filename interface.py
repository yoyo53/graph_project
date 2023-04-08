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
        self.graph_frame = Frame(self.content)
        self.graph_frame.grid(row=0, pady=10)
        Label(self.graph_frame, fg='black', font=('Arial', 16), justify="center", text="No graph selected").pack()
        self.analyze_frame = Frame(self.content)
        self.button_frame = Frame(self.content)
        self.button_frame.grid(row=2, pady=10)
        Button(self.button_frame, text='Load graph', command=self.load_graph).grid(row=0, column=0, padx=10)
        self.analyze_button = Button(self.button_frame, text='Analyze graph', command=self.analyze_graph)

    def load_graph(self):
        self.filepath = askopenfilename(filetypes=[("text files", "*.txt")], initialdir="./test files/")
        if self.filepath is None or self.filepath == "":
            showinfo("Warning", "No file selected !")
        else:
            self.graph = Graph(self.filepath)
            self.add_graph_table()

    def add_graph_table(self):
        for child in self.graph_frame.winfo_children():
            child.destroy()
        self.analyze_frame.grid_forget()
        self.analyze_button.grid(row=0, column=1, padx=10)
        Label(self.graph_frame, fg='black', font=('Arial', 12), justify="center", text=f"Graph from file {self.filepath.split('/')[-1]}").grid(row=0, column=0, pady=10, columnspan=2)
        matrix = self.graph.as_matrix()
        sizes = [max(map(len, col)) + 3 for col in zip(*matrix)]
        table_frame = Frame(self.graph_frame)
        table_frame.grid(row=1, column=0, padx=10)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != "*":
                    color = 'blue'
                else:
                    color = 'black'
                Label(table_frame, width=sizes[j], fg=color, font=('Arial', 12), justify="center", text=matrix[i][j], relief=RAISED).grid(row=i, column=j)
        as_list = str(self.graph).split("\n")
        max_rows = int(1.4 * len(self.graph.vertices))
        if len(as_list) > max_rows:
            for i in range(0, len(as_list), max_rows):
                Label(self.graph_frame, fg='black', font=('Arial', 12), justify="left", text="\n".join(as_list[i:i+max_rows])).grid(row=1, column=int(1 + i/max_rows), sticky=NW, padx=10)
        else:
            Label(self.graph_frame, fg='black', font=('Arial', 12), justify="left", text=self.graph).grid(row=1, column=1, sticky=NW, padx=10)

    def analyze_graph(self):
        self.analyze_frame.grid(row=1)
        for child in self.analyze_frame.winfo_children():
            child.destroy()
        self.analyze_button.grid_forget()
        if not self.graph.is_scheduling() or self.graph.has_cycle():
            lines = [
                "This is not a scheduling graph. A scheduling graph must satisfy the following conditions:",
                "    - a single entry point,",
                "    - a single exit point,",
                "    - no cycle,",
                "    - same weights for all outgoing edges of a vertex,",
                "    - outgoing edges of the entry vertex have zero,",
                "    - no negative edges."
            ]
            Label(self.analyze_frame, fg='black', font=('Arial', 12), justify="left", text="\n".join(lines)).grid()
        else:
            lines = [
                "This is a scheduling graph with no cycle and no negative edges."
            ]
            matrix = [["vertex"] + [vertex.name for vertex in self.graph.vertices]]
            matrix += [["rank"] + [str(rank) for rank in self.graph.get_rank()]]
            matrix += [["earliest date"] + [str(date) for date in self.graph.get_earliest_date()]]
            matrix += [["latest date"] + [str(date) for date in self.graph.get_latest_date()]]
            matrix += [["total float"] + [str(Float) for Float in self.graph.get_total_float()]]
            matrix += [["free float"] + [str(Float) for Float in self.graph.get_free_float()]]
            sizes = [max(map(len, col)) + 2 for col in zip(*matrix)]
            table_frame = Frame(self.analyze_frame)
            table_frame.grid(row=0, column=0, padx=10)
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    Label(table_frame, width=sizes[j], fg='blue', font=('Arial', 12), justify="center", text=matrix[i][j], relief=RAISED).grid(row=i + 1, column=j)
            critical_paths = self.graph.get_critical_path()
            if len(critical_paths) > 1:
                lines += ["The critical paths are:"]
            else:
                lines += ["The critical path is:"]
            for path in self.graph.get_critical_path():
                lines.append("    - " + " --> ".join(str(vertex) for vertex in path))
            Label(self.analyze_frame, fg='black', font=('Arial', 12), justify="left", text="\n".join(lines)).grid(row=0, column=1, pady=10, sticky=NW)
