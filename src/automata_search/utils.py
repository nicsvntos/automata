import graphviz
import string
import random

def create_automata_diagram(pattern):
    """
    creates a diagram object showing the dfa for the pattern
    Args:
        pattern (_type_): _description_
    """

    from dfa import compute_lps_array

    lps = compute_lps_array(pattern)
    dot = graphviz.Digraph(comment='KMP Automata')
    dot.attr(rankdir='LR') #left to right
    dot.attr('node', shape='circle')

    dot.node('', shape='none', height='.0', width='.0')
    dot.edge('','0')

    for i in range(len(pattern) + 1):
        shape = 'doublecircle' if i == len (pattern) else 'circle'
        dot.node(str(i), shape=shape)


    for i in range (len(pattern)):
        current_state = i
        next_state = i + 1
        char = pattern[i]

        dot.edge(str(current_state), str(next_state), label=f"{char}")

        if i > 0:
            fail_state = lps[1]

            if fail_state != 0:
                dot.edge(str(i+1), str(fail_state), style='dashed', label=f"miss", constraint='false')
            else:
                dot.edge(str(i+1), '0', style='dashed', label="miss", constraint = 'false')
    dot.edge('0', '0', label=f"!{pattern[0]}", style = 'dotted', color='grey')

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