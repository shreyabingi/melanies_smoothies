import streamlit as st
from snowflake.snowpark.context import get_active_session

# Title
st.title("Customize your Smoothie 🎈")

# Get Snowflake session
session = get_active_session()

# Load fruit list
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")

fruit_list = fruit_df.select("FRUIT_NAME") \
                     .to_pandas()["FRUIT_NAME"] \
                     .tolist()

# Name input
name_on_order = st.text_input("Name on Order")

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 Ingredients:",
    fruit_list,
    max_selections=5
)

ingredients_string = ", ".join(ingredients_list)

if ingredients_string:
    st.write("Your smoothie will contain:")
    st.write(ingredients_string)

# Submit order
if st.button("Submit Order"):

    if not name_on_order:
        st.error("Please enter your name.")

    elif not ingredients_string:
        st.error("Please choose ingredients.")

    else:

        insert_stmt = f"""
            insert into smoothies.public.orders
            (ingredients, name_on_order)
            values ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_stmt).collect()

        st.success(
            f"Your Smoothie for {name_on_order} is ordered! ✅"
        )
