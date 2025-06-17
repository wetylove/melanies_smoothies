import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Titre et instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Champ pour le nom
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connexion Snowflake
cnx = st.connection("snowflake")
session = cnx.session()  # Connexion via Streamlit Cloud

# Récupération des données
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe.collect()]  # liste de chaînes

# Multiselect - liste des fruits
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_names, max_selections=5)

# Gestion de la commande
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)  # Affichage SQL pour debug

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        st.stop()
