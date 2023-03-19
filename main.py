from graph import Graph
from interface import Interface

graph = Graph('test files/table 1.txt')
print(graph)
print(graph.as_formatted_matrix())
print(graph.has_a_cycle())

if not graph.is_scheduling():
    lines = [
        "This is not a scheduling graph. A scheduling graph must satisfies the following conditions:",
        "    - a single entry point,",
        "    - a single exit point,",
        "    - no cycle,",
        "    - same weights for all outgoing edges of a vertex,",
        "    - outgoing edges of the entry vertex have zero,",
        "    - no negative edges."
    ]
    print("\n".join(lines))
else:
    print("This is a scheduling graph with no cycle and no negative edges.")
    matrix = [["vertex"] + [vertex.name for vertex in graph.vertices]]
    matrix += [["rank"] + [str(rank) for rank in graph.get_rank()]]
    matrix += [["earliest date"] + [str(date) for date in graph.get_earliest_date()]]
    matrix += [["latest date"] + [str(date) for date in graph.get_latest_date()]]
    matrix += [["total float"] + [str(Float) for Float in graph.get_total_float()]]
    matrix += [["free float"] + [str(Float) for Float in graph.get_free_float()]]
    sizes = [max(map(len, col)) for col in zip(*matrix)]
    fmt = " | ".join(f"{{:{size}}}" for size in sizes)
    lines = [fmt.format(*row) for row in matrix]
    print("\n".join(lines))
    critical_paths = graph.get_critical_path()
    if len(critical_paths) > 1:
        print("The critical paths are:")
    else:
        print("The critical path is:")
    for path in graph.get_critical_path():
        print("    - " + " --> ".join(str(vertex) for vertex in path))

if __name__ == '__main__':
    interface = Interface()
    interface.mainloop()
