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
pattern = st.sidebar.text_input("Enter Search Pattern", value="ABAB")

st.divider()

#visualization section
st.header("Finite Automata(DFA)")

if pattern:
    #generate a graph using the utils function
    graph = utils.create_automata_diagram(pattern)
    st.graphviz_chart(graph)

    #display lps array
    lps = dfa.compute_lps_array(pattern)
    st.text(f"Computed LPS Array for '{pattern}': {lps}")
else:
    st.warning("Please enter a pattern in the sidebar to generate the Automata")

st.divider()

#file search section

st.header("Single File Search")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input File")
    uploaded_file = st.file_uploader("Upload a .txt file(1MB - 10MB)", type=['txt'])

    #button for the search filez
    if st.button("Search Uploaded File",type="primary", use_container_width=True):
        if uploaded_file and pattern:

            #read file
            string_data = uploaded_file.read().decode("utf-8")
            file_size_mb = len(string_data) / (1024 * 1024)

            #perform search with timer
            with st.spinner(f"Searching {file_size_mb:.2f} MB File..."):
                start_time = time.time()
                matches = dfa.kmp_search(string_data, pattern)
                end_time = time.time()
            
            time_taken = end_time - start_time

            #display results
            st.success ("Search complete!")
            st.metric("Matches Found", matches)
            st.metric("Time taken (seconds)", f"{time_taken:.4f}")

        else:
            st.error ("Please upload a file and enter a pattern")

with col2:
    st.subheader("Algorithm info")
    st.info("KMP Algorithm")
st.divider()

#big-o analysis section
st.header("Big-O Performance Analysis")
st.markdown("click below to automatically generate files of increasing size and chart the performance")

if st.button("Run Big-O Simulation", use_container_width=True):
    if not pattern:
        st.error ("Please enter a pattern in the sidebar first")
    else:
        #define sizes to test (in MB)
        sizes_mb = [1,2,5,10]
        time_results = []

        #create a placeholder for the progress bar
        bar_placeholder = st.empty()
        progress_bar = bar_placeholder.progress(0)

        st.write("Generating files and running search...")

        for i, size in enumerate(sizes_mb):

            #generate temporary file
            temp_filename = f"temp_test{size}mb.txt"
            utils.generate_test_file(temp_filename, size)

            #read file
            with open (temp_filename, 'r', encoding='utf-8') as f:
                data = f.read()
            
            #run search

            start = time.time()
            dfa.kmp_search(data, pattern)
            end = time.time()

            elapsed = end - start
            time_results.append(elapsed)

            #delete temp file
            os.remove(temp_filename)

            #update progress file
            progress_bar.progress((i + 1) / len (sizes_mb))
        
        #clear progress bar
        bar_placeholder.empty()

        #display chart
        st.subheader("Results")
        st.line_chart(data=time_results, use_container_width=True)

        st.write("Analysis")
        st.write(f"Pattern: '{pattern}'")
        st.write("X-axis: File Size (1MB, 2MB, 5MB, 10MB)")
        st.write("Y-Axis: Time (seconds)")

        if len (time_results) > 1:
            ratio = time_results[-1] / time_results[0]
            size_ratio = sizes_mb[-1] / sizes_mb[0]
            st.success(f"Performance Check: Increasing file size by {size_ratio} * increased time by {ratio:.2f}. This indicates O(n) complexity")
