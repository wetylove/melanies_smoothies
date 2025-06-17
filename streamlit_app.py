import streamlit as st

from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get user input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get session and data
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe.collect()]
cnx = st.connection("snowflake")
session = cnx.session()
# Multiselect UI
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)


if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # Proper INSERT SQL statement
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    # Submission logic
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        st.stop()
