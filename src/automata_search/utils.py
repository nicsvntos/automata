import graphviz
import string
import random

def create_automata_diagram(pattern, path_history=None):
    """
    creates a diagram object showing the dfa for the pattern
    Args:
        pattern (_type_): _description_
    """

    from dfa import compute_lps_array

    lps = compute_lps_array(pattern)
    dot = graphviz.Digraph(comment='KMP Automata')
    dot.attr(rankdir='LR') #left to right
    dot.attr(size='12.4')
    dot.attr(ranksep='0.5')
    dot.attr(nodesep='0.8')

    if path_history is None:
        edge_color = 'black'
        font_color = 'black'
    else:
        edge_color = 'lightgrey'
        font_color = 'lightgrey'

    for i in range(len(pattern) + 1):
        shape = 'doublecircle' if i == len (pattern) else 'circle'
        dot.node(str(i), shape=shape)

    def add_edge(u,v,label,style='solid', constraint='true'):
        dot.edge(str(u), str(v), label=label, style=style, color=edge_color, fontcolor=font_color, constraint=constraint)

    dot.node ('', shape='none', height='.0', width='.0')
    add_edge('', '0', label='', style='bold')

    for i in range (len(pattern)):
        add_edge(i,i+1,pattern[i])

    for i in range(len(pattern)):
        if i > 0:
            fail_state = lps[i]
            if fail_state != 0:
                add_edge(i+1, fail_state, "miss", style='dashed', constraint='false')
            else:
                add_edge(i + 1, 0, "miss", style='dashed', constraint='false')
    
    add_edge (0,0, f"!{pattern[0]}", style='dotted', constraint='false')

    if path_history:
        for step in path_history:
            u = step ['from']
            v = step ['to']
            label = step ['char']
            ptype = step['type']

            color = 'green'
            width = '2.0'

            if ptype == 'mismatch' or ptype == 'reset':
                color = 'red'
                width = '2.0'

            dot.edge(str(u), str(v), label=label, color=color, penwidth=width)

            if ptype != 'mismatch':
                dot.node(str(v), color = color, pendwidth='2.5')
    
    return dot

def generate_test_file(filename, size_mb):
    """
    generates a test dummy file

    Args:
        filename (_type_): _description_
        size_mb (_type_): _description_
    """

    target_size = size_mb * 1024 * 1024

    chunk_size = 1024 * 1024
    chars = string.ascii_letters + string.digits + ' '

    with open (filename, 'w', encoding= 'utf-8') as f:
        written = 0
        while written < target_size:
            chunk = ''.join(random.choice(chars) for _ in range (chunk_size))
            f.write(chunk)
            written += len(chunk)
    
    return f"Generated {filename} ({size_mb}MB)"