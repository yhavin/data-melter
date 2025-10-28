
"""
Streamlit app for splitting and unpivoting wide tables of contacts.

Author: Yakir Havin
"""


import streamlit as st
import polars as pl


# =======================
# Functions
# =======================
def melt_data(df: pl.DataFrame, on: str) -> pl.DataFrame:
    """Split phone numbers and convert to long format."""
    df = df.with_columns(
        pl.col(on).str.split(" \n")  # Typically the phone number delimiter is " \n"
    )
    df = df.explode(on)

    df = df.with_columns(
        pl.col(on).str.split("\n")  # Also need to handle "\n" delimiter (no-op for previously split rows)
    )
    df = df.explode(on)

    df = df.rename({"Alt Phone", "Phone Number"})

    after_length = df.shape[0]
    data = df.write_csv()
    return data, after_length


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Data Melter",
    page_icon=":material/data_table:"
)

st.header(":material/data_table: Data Melter")
st.caption("Developed by Yakir Havin")

# with st.expander(label="💡 Instructions"):
#     st.markdown(
#         """
#         1. Upload a CSV of the contacts data
#         2. Select the column containing multiple phone numbers
#         3. Press Run
#         4. Download expanded CSV
#         """
#     )

with st.container(border=True):
    input_file = st.file_uploader(
        label="Upload file",
        type="csv"
    )

    if input_file is not None:
        print(input_file)
        df = pl.read_csv(input_file, ignore_errors=True)
        headers = df.columns
        before_length = df.shape[0]

        on_column = st.selectbox(
            label="Choose phone numbers column",
            options=headers,
            index=None
        )

        submit = st.button(
            label="Run",
            icon=":material/play_circle:"
        )

        if submit:
            data, after_length = melt_data(df, on_column)
            message = f"Successfully expanded {before_length} rows into {after_length} contacts."
            print(message)
            st.success(body=message)

            download_button = st.download_button(
                label="Download",
                data=data,
                icon=":material/download:",
                mime="text/csv",
                file_name="contacts.csv"
            )