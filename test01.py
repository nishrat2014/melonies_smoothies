# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark.functions import col
import pandas as pd
import snowflake.connector


# Write directly to the app
st.title(f"🥤 Customize your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input('Name on smoothie;')
st.write('The name of smoothie will be:', name_on_order)

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)
#snowflake connection
conn = snowflake.connector.connect(
  user=st.secrets["snowflake"]["user"],

password=st.secrets["snowflake"]["password"],

account=st.secrets["snowflake"]["account"],

warehouse=st.secrets["snowflake"]["warehouse"],

database=st.secrets["snowflake"]["database"],

schema=st.secrets["snowflake"]["schema"],

# Get fruit options
df = pd.read_sql("SELECT FRUIT_NAME FROM FRUIT_OPTIONS", conn)


ingredients_list = st.multiselect (
    'Chose upto 5 ingredeitns:'
    ,df["FRUIT_NAME"].TOLIST()
    ,max_selections= 5
)

if ingredients_list and name_on_order:

    #st.write(ingredients_list)
    #st.text(ingredients_list)

   ingredients_string="".join(ingredients_list)

      if st.button("Submit Order"):
                   cursor=conn.cursor()
                   cursor.execute("""INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
                                      values ($s,$s)""",
      (ingredients_string, name_on_order)
                                 )
                  cursor.close()

 
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")




    
