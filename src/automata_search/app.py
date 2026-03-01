import streamlit as st
import os
import dfa, utils
import time

st.set_page_config(
    page_title="DFA Visualizer",
    layout="wide"
)

#main ui

st.title ("KMP Algorithm and DFA Visualizer")

#sidebar inputs
st.sidebar.header("Configuration")

#pattern input
pattern = st.sidebar.text_input("Input Search Pattern", value="ABAB")

st.divider()

#text input
st.sidebar.subheader("Visualization Mode")
st.sidebar.write("Input Text Pattern to see the path traced:")
demo_text = st.sidebar.text_area("Small Text Input", height=100, placeholder="e.g. ABABAC")

st.sidebar.divider()

#file upload for big-o notation
st.sidebar.subheader("Performance Mode")
st.sidebar.write("Upload a file for speed analysis")
uploaded_file = st.sidebar.file_uploader("File (1MB-10MB)", type=['txt'])

#button
run_btn = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

#main app logic

if pattern:

    mode = "idle"
    results = None

    if run_btn:
        if demo_text:
            mode = "visualization"
            #kmp with path tracing
            matches, path_history = dfa.kmp_search_with_path(demo_text, pattern)

            st.session_state.demo_results = {
                'matches': matches,
                'path': path_history,
                'data': demo_text,
                'pattern': pattern
            }
        
        elif uploaded_file:
            mode = "performance"
            #read file
            string_data = uploaded_file.read().decode("utf-8")
            #run kmp
            start_time = time.time()
            matches = dfa.kmp_search(string_data, pattern)
            end_time = time.time()
            time_taken = end_time - start_time
            results = {'matches': matches, 'time': time_taken, 'size_mb': len(string_data)/(1024*1024)}

        else:
            st.sidebar.warning("Please enter text or upload a file")

    #display automata graph
    st.header("Finite Automate(DFA) & LPS Table")
    lps = dfa.compute_lps_array (pattern)

    table_data = {
        "Pattern Char": list(pattern),
        "LPS Value": lps
    }
    col_graph, col_table = st.columns([3,1])

    with col_graph:
        history_to_draw = results ['path'] if (mode == "visualization" and results) else None
        graph = utils.create_automata_diagram(pattern, path_history=history_to_draw)
        st.graphviz_chart(graph)
    
    with col_table:
        st.subheader("LPS Array")
        st.dataframe(table_data, use_container_width=True)

        st.caption ("Longest Prefix Suffix")
        st.caption ("Tells the algorithm how far back to jump on mismatch")

    st.divider()

    #diplay results area
    
    #case 1: visualization results
    if 'demo_results' in st.session_state:
        results = st.session_state.demo_results
        full_path = results['path']
        total_steps = len(full_path)

        st.header("Visual Trace")

        if total_steps > 0:
            col1, col2 = st.columns([3,1])

            with col1:
                #animation slider
                #shows the total steps first
                current_step = st.slider (
                    "Step Through Animation",
                    min_value = 0,
                    max_value= total_steps,
                    value= total_steps,
                    format = "Current Step: %d"
                )

                st.caption(f"Total Steps: {total_steps}")
                #create the graph using only the path up to the current slider value

                current_path_slice = full_path[:current_step]

                graph = utils.create_automata_diagram(
                    results['pattern'],
                    path_history=current_path_slice
                )
                st.graphviz_chart(graph)
        
            with col2:
                st.metric("Total Matches", results['matches'])

                #show details of the *current* step based on the slider position

                if current_step > 0:
                    last_move = full_path[current_step - 1]

                    st.subheader("Current Step:")

                    icon = "✅" if last_move['type'] == 'match' else "🔄"
                    if last_move['type'] == 'reset': icon = "🏁"

                    st.markdown(f"**{icon} Transition**")
                    st.text(f"From: State {last_move['from']}")
                    st.text(f"To: State {last_move['to']}")
                    st.text(f"Char: '{last_move['char']}")

                    st.divider()

                    #show history log
                    st.text("History:")
                
                    #show the last 5 moves relative to the slider
                    recent = full_path[max(0, current_step - 5) : current_step]
                    for move in recent:
                        st.caption(f" -> State {move['to']}")
            
                else:
                    st.info("Drag slider to start")
        else:
            st.warning ("No steps to visualize. Please enter a valid text in the sidebar")        

    #case 2: performance results
    elif mode == "performance" and results:
        st.header("Performance Metrics")

        col1, col2, col3, = st.columns(3)
        col1.metric("File Size", f"{results['size_mb']:.2f} MB")
        col2.metric("Matches Found", results ['matches'])
        col3.metric("Time Taken", f"{results['time']:.4f} sec")

    #case 3: big-o simulation
    st.divider()
    st.header("Big-O Simulation")
    st.markdown("Generate files of increasing size to test linear complexity")

    if st.button("Run Big-O Simulation", use_container_width=True):
        if not pattern:
            st.error("Please enter pattern in the sidebar first.")
        else:
            sizes_mb = [1,2,5,10]
            time_results = []
            bar_placeholder = st.empty()
            progress_bar = bar_placeholder.progress(0)

            st.write ("Generating temporary files and running search...")

            for i, size in enumerate(sizes_mb):
                temp_filename = f"temp_test_{size}mb.txt"
                utils.generate_test_file(temp_filename, size)

                with open (temp_filename, 'r', encoding='utf-8') as f:
                    data = f.read()

                start = time.time()
                dfa.kmp_search(data, pattern)
                end = time.time()

                elapsed = end - start
                time_results.append(elapsed)
                os.remove(temp_filename)

                progress_bar.progress((i + 1) / len(sizes_mb))

            bar_placeholder.empty()

            st.subheader("Performance Chart")
            st.line_chart(data = time_results, use_container_width=True)

            if len (time_results) > 1:
                ratio = time_results[-1] / time_results[0]
                size_ratio = sizes_mb[-1] / sizes_mb[0]
                st.success(f"Analysis: Increasing size by {size_ratio}x increased time by {ratio:.2f}x. Indicates O(n) complexity.")
    
else:
    st.info("Please input a pattern in the sidebar to start.")
