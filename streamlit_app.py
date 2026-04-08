import streamlit as st

# Title
st.title("Customize your Smoothie 🎈")

# Local fruit list (instead of Snowflake table)
fruit_list = [
    "Apple",
    "Banana",
    "Blueberries",
    "Strawberries",
    "Mango",
    "Kiwi",
    "Dragon Fruit",
    "Guava",
    "Figs",
    "Cantaloupe"
]

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
        st.success(
            f"Your Smoothie for {name_on_order} is ordered! ✅"
        )
