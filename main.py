import os
import time
import streamlit as st
from streamlit_option_menu import option_menu
from tools.gridding import grid_vel, create_vts

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Tool Bar",
            options=["Home", "Gridding", "Stacking", "Inversion"],
            menu_icon="cast",
            default_index=0
        )

    if selected == "Home":
        st.title("Seismic Tomography Toolkit")
        st.write("By Kevin Ryano (@kevinryano)")
        st.markdown("---")

    if selected == "Gridding":
        st.title("Gridding")
        st.write("Tomogram gridding tools")
        st.markdown("---")

        delta = st.number_input("Input Delta XYZ", min_value=10, max_value=100, step=5)
        interp_method = st.radio("Input Interpolation Method", options=['linear', 'rbf'])

        nama_file_grid = st.text_input("File Output Name")
        veldat = st.file_uploader("Upload Velocity Data", type=["csv"])
        gridBtn = st.button("Start Gridding")

        if gridBtn:
            t0 = time.perf_counter()
            x, y, z, vp, vs, ps = grid_vel(veldat, delta=int(delta), interp_method=interp_method)
            create_vts(x, y, z, vp, vs, ps, nama_file=nama_file_grid)
            t1 = time.perf_counter()

            with open(nama_file_grid+".vts", "rb") as file_vts:
                downloadBtn = st.download_button(label="Download VTS File",
                                                 data=file_vts,
                                                 file_name=nama_file_grid+".vts")
                if downloadBtn:
                    file_vts.close()
                    os.remove(nama_file_grid+".vts")
            st.markdown("***")
            st.text(f"========== {nama_file_grid}.vts Created ==========\n")
            st.text(f"> Interpolation Method \t: {interp_method}")
            st.text(f"> Runtime \t\t: {t1-t0:.2f} s")

    if selected == "Stacking":
        st.title("Stacking App")
        st.markdown("---")
        st.write("Coming Soon...")

    if selected == "Inversion":
        st.title("Inversion App")
        st.markdown("---")
        st.write("Coming Soon..")

if __name__ == "__main__":
    main()