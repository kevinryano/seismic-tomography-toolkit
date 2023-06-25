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

        cols = st.columns(3)

        delta_x = cols[0].number_input("Input Delta X", min_value=10, max_value=100, step=5)
        delta_y = cols[1].number_input("Input Delta Y", min_value=10, max_value=100, step=5)
        delta_z = cols[2].number_input("Input Delta Z", min_value=10, max_value=100, step=5)

        veldat = st.file_uploader("Upload Velocity Data", type=["csv"])
        interp_method = st.radio("Input Interpolation Method", options=['linear', 'rbf'])

        gridBtn = st.button("Start Gridding")
        if gridBtn:
            t0 = time.perf_counter()
            x, y, z, vp, vs, ps = grid_vel(veldat,
                                           deltax=int(delta_x),
                                           deltay=int(delta_y),
                                           deltaz=int(delta_z),
                                           interp_method=interp_method)
            create_vts(x, y, z, vp, vs, ps, nama_file="temp")
            t1 = time.perf_counter()

            st.text("========== Process Done ==========")
            st.text(f"> Interpolation Method \t: {interp_method}")
            st.text(f"> Processing Time \t: {t1 - t0:.2f} s")

            nama_file_grid = st.text_input("Output File Name")
            with open("temp.vts", "rb") as file_vts:
                downloadBtn = st.download_button(label="Download VTS",
                                                 data=file_vts,
                                                 file_name=f"{nama_file_grid}.vts")
                if downloadBtn:
                    st.markdown("***")
                    st.text(f"{nama_file_grid}.vts created")
                    # time.sleep(30)
                    file_vts.close()
                    os.remove("temp.vts")

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