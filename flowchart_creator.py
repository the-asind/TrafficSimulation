import graphviz
def create_flowchart():
    dot = graphviz.Digraph()

    # Set global graph properties
    dot.attr('graph', rankdir='LR', splines='ortho')

    # Nodes
    dot.node('Start', shape='oval')
    dot.node('Generate Car Arrivals', shape='box')
    dot.node('Loop', shape='hexagon')
    dot.node('Condition 1', shape='diamond')
    dot.node('Process Car 1', shape='box')
    dot.node('Condition 2', shape='diamond')
    dot.node('Process Car 2', shape='box')
    dot.node('Add Waiting Time', shape='box')
    dot.node('Calculate Average', shape='box')
    dot.node('End', shape='oval')

    # Edges
    dot.edge('Start', 'Generate Car Arrivals')
    dot.edge('Generate Car Arrivals', 'Loop')
    dot.edge('Loop', 'Condition 1', label='elapsed_time < simulation_duration', xlabel=' ', dir='forward')
    dot.edge('Condition 1', 'Process Car 1', xlabel='Car Arrival', dir='forward')
    dot.edge('Process Car 1', 'Condition 1', dir='forward')
    dot.edge('Condition 1', 'Condition 2', xlabel='No More Cars', dir='forward')
    dot.edge('Condition 2', 'Process Car 2', xlabel='Car Arrival', dir='forward')
    dot.edge('Process Car 2', 'Condition 2', dir='forward')
    dot.edge('Condition 2', 'Loop', xlabel='No More Cars', dir='forward')
    dot.edge('Loop', 'Add Waiting Time', label='elapsed_time >= simulation_duration', xlabel=' ', dir='forward')
    dot.edge('Add Waiting Time', 'Calculate Average')
    dot.edge('Calculate Average', 'End')

    dot.render('flowchart', format='png', view=True)


create_flowchart()
