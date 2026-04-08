import streamlit as st
from snowflake.snowpark.context import get_active_session

# Title
st.title("Customize your Smoothie :balloon:")

# Snowflake session
session = get_active_session()

# Load fruit table
fruit_df = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
)

fruit_list = (
    fruit_df
    .select("FRUIT_NAME")
    .to_pandas()["FRUIT_NAME"]
    .tolist()
)

# Name input
name_on_order = st.text_input("Name on Order")

# Favorite fruit dropdown
option = st.selectbox(
    "What is your favourite fruit?",
    fruit_list
)

st.write("Your favourite fruit is:", option)

# Multi-select ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 Ingredients:",
    fruit_list,
    max_selections=5
)

# Extra safety validation
if len(ingredients_list) > 5:
    st.error("Please select no more than 5 fruits.")
    st.stop()

# Convert list to string
ingredients_string = ", ".join(ingredients_list)

# Show ingredients
if ingredients_string:
    st.write("Your smoothie will contain:")
    st.write(ingredients_string)

# Submit button
if st.button("Submit Order"):

    if not name_on_order:
        st.error("Please enter your name.")

    elif not ingredients_string:
        st.error("Please choose ingredients.")

    else:

        # Escape single quotes (important)
        safe_name = name_on_order.replace("'", "''")

        my_insert_stmt = f"""
        insert into smoothies.public.orders
        (ingredients, name_on_order)
        values ('{ingredients_string}', '{safe_name}')
        """

        # Debug output
        st.write("Running SQL:")
        st.code(my_insert_stmt)

        # Execute insert
        session.sql(my_insert_stmt).collect()

        st.success(
            f"Your Smoothie for {name_on_order} is ordered!",
            icon="✅"
        )
