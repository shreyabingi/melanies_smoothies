import streamlit as st
import snowflake.connector

# Snowflake connection (use secrets)
conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

cur = conn.cursor()

# Title
st.title("Customize your Smoothie 🎈")

# Load fruits from Snowflake
cur.execute("SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS")

fruit_list = [row[0] for row in cur.fetchall()]

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

        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        cur.execute(insert_sql)
        conn.commit()

        st.success(
            f"Your Smoothie for {name_on_order} is ordered! ✅"
        )
