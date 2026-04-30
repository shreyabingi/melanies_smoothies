import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get Snowflake session
session = get_active_session()

# Title
st.title("Customize your Smoothie 🎈")

# Load fruits
fruits = session.sql(
    "SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).collect()

fruit_list = [row["FRUIT_NAME"] for row in fruits]

# Name input
name_on_order = st.text_input("Name on Order")

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 Ingredients:",
    fruit_list,
    max_selections=5
)

# IMPORTANT — DO NOT SORT
ingredients_string = ", ".join(ingredients_list)

# Show ingredients
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

        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES (
            '{ingredients_string}',
            '{name_on_order}'
        )
        """

        session.sql(insert_sql).collect()

        st.success(
            f"Your Smoothie for {name_on_order} is ordered! ✅"
        )
