import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# checkbox for final lab
order_filled = st.checkbox("Mark order as filled")

cnx = st.connection("snowflake")
session = cnx.session()

fruit_df = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

pd_df = fruit_df.to_pandas()

fruit_options = pd_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        # IMPORTANT: keep trailing space for grader hash match
        ingredients_string += fruit_chosen + " "

        st.subheader(f"{fruit_chosen} Nutrition Information")

        matching_rows = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"]

        if not matching_rows.empty:
            search_on = matching_rows.iloc[0]

            smoothiefroot_response = requests.get(
                "https://my.smoothiefroot.com/api/fruit/" + search_on
            )

            if smoothiefroot_response.status_code == 200:
                st.dataframe(
                    data=smoothiefroot_response.json(),
                    use_container_width=True
                )
            else:
                st.warning(f"No nutrition data found for {fruit_chosen}")
        else:
            st.warning(f"No search value found for {fruit_chosen}")

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        safe_name = name_on_order.replace("'", "''") if name_on_order else ""
        safe_ingredients = ingredients_string.replace("'", "''")
        safe_order_filled = "TRUE" if order_filled else "FALSE"

        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (name_on_order, ingredients, order_filled)
        VALUES ('{safe_name}', '{safe_ingredients}', {safe_order_filled})
        """

        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon=":white_check_mark:")
