import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents\' New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),default=['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display Fruityvice API response
streamlit.header("View our fruit list - Add your favorites!")

def get_fruityvice_data (this_fruit_choice):
    # streamlit.write('The user entered ', this_fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # streamlit.text(fruityvice_response.json())
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error

# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur
        # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cns.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list ('" + new_fruit + "')")
        return 'Thanks for adding ' + new_fruit

fruit_insert = streamlit.text_input('What fruit would you like to add?','user choice')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_insert)
    my_cnx.close()
    streamlit.text(back_from_function)

streamlit.stop()
cur_fruit_insert = my_cnx.cursor()
cur_fruit_insert.execute('insert into fruit_load_list (fruit_name) values (' + fruit_insert + ');')
streamlit.text("Thanks for adding" + fruit_insert)
