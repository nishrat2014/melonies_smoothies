# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark.functions import col
import pandas as pd
import snowflake.connector
import requests


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
)
# Get fruit options
df = pd.read_sql("SELECT FRUIT_NAME, SEARCH_ON FROM FRUIT_OPTIONS", conn)
st.dataframe(data=df,  use_container_width=True)

st.dataframe(pd_df)
st.stop()



ingredients_list = st.multiselect (
    'Chose upto 5 ingredeitns:'
    ,df["FRUIT_NAME"].tolist()
    ,max_selections= 5
)


# Loop through each selected fruit
for fruit_chosen in ingredients_list:
    # Show subheader
    st.subheader(f"{fruit_chosen} nutrition information")

    # Call API for that fruit
    response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}")
    if response.status_code == 200:
        fruit_json = response.json()
        
       
        # Build rows: one row per nutrient
        rows = []
        for nutrient, value in fruit_json.get("nutrition", {}).items():
            rows.append({
                "": nutrient,  # first column has no header
                "family": fruit_json.get("family"),
                "genus": fruit_json.get("genus"),
                "id": fruit_json.get("id"),
                "name": fruit_json.get("name"),
                "nutrition": value,
                "order": fruit_json.get("order"),
            })

        # Convert to DataFrame and display
        sf_df = pd.DataFrame(rows).set_index("")
        st.dataframe(sf_df, use_container_width=True)



if ingredients_list and name_on_order:
    ingredients_string = "".join(ingredients_list)

    if st.button("Submit Order"):
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
               VALUES (%s, %s)""",
            (ingredients_string, name_on_order)
        )
        cursor.close()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")





    
