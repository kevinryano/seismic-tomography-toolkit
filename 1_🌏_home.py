import os
import time

import pandas as pd
import streamlit
import streamlit as st
from streamlit_option_menu import option_menu
from tools.gridding import grid_vel, create_vts

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Bar",
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

        st.subheader("Upload Velocity Data")
        veldat = st.file_uploader("Upload Velocity Data", type=["csv"], label_visibility='hidden')

        # dfBtn = st.button("Show Dataframe")
        #
        # if dfBtn:
        #     veldat_c = veldat
        #     st.dataframe(pd.read_csv(veldat_c), use_container_width=True)
        #     # veldat_c.close()

        st.markdown("***")
        st.subheader("Input Parameter")
        cols = st.columns(3)

        delta_x = cols[0].number_input("Delta X", min_value=10, max_value=100, step=5)
        delta_y = cols[1].number_input("Delta Y", min_value=10, max_value=100, step=5)
        delta_z = cols[2].number_input("Delta Z", min_value=10, max_value=100, step=5)

        interp_method = st.radio("Input Interpolation Method", options=['linear', 'rbf'])

        nama_file_grid = st.text_input("Output File Name")
        st.write(" ")

        gridBtn = st.button("Start Gridding")
        if gridBtn:
            t0 = time.perf_counter()
            x, y, z, vp, vs, ps = grid_vel(data=veldat,
                                           deltax=int(delta_x),
                                           deltay=int(delta_y),
                                           deltaz=int(delta_z),
                                           interp_method=interp_method)
            create_vts(x, y, z, vp, vs, ps, nama_file=nama_file_grid)
            t1 = time.perf_counter()

            st.markdown("***")
            st.markdown("=============== Process Done ===============")
            st.markdown(f"> Interpolation Method   :   {interp_method}")
            st.markdown(f"> Compute Time   :   :green[{t1 - t0:.2f}] s")
            st.markdown(f">**{nama_file_grid}.vts**  successfully  created")
            st.markdown("***")

            st.markdown("**:red[File is ready to be downloaded]**")
            with open(f"{nama_file_grid}.vts", "rb") as file_vts:
                downloadBtn = st.download_button(label="Download VTS",
                                                 data=file_vts,
                                                 file_name=f"{nama_file_grid}.vts")
                file_vts.close()
                os.remove(f"{nama_file_grid}.vts")

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