
# Import all from fasthtml.common
from fasthtml.common import *

# Import pandas
import pandas as pd

# Initialize a fasthtml app
app, route = fast_app()

# Using pandas, read in he 'ds_event.csv' file
df = pd.read_csv('ds_events.csv')

# Define a route for the landing page
# that uses a `get` method
@app.route("/")
def get():

    # Generate the raw html for the pandas table
    # with the pandas .to_html method
    table_html = df.to_html()

    # Convert the raw html to a fasthtml object
    # using the fasthtml NotStr function
    table = NotStr(table_html)

    # Using the `Titled` fasthtml function
    # Set the title of the page to an informative
    # title for the data, and pass the fasthtml table
    # as the second argument
    # Return the result
    return Titled(
        "Data Science Events!",
        table,
        )

# Define a route with a dynamic
# `keyword` variable that can be passed
# to the routing function
# Include a `date` query parameter
@app.route("/search/{keyword}")
def get(keyword:str, date:str=None):

    # Filter the pandas dataframe to rows where the 
    # `description` column contains the `keyword`
    # received as an argument to this function
    frame = df[df.description.str.lower().str.contains(keyword)]

    # Check if date is "truthy"
    if date:

        # Filter the dataframe down to rows
        # where the `date` column is equal to the date
        # query parameter
        frame = frame[frame.date == date]
    
    # Convert the filtered dataframe to
    # a list of dictionaries
    json = frame.to_dict(orient='records')

    # Return the data as a json response
    return JSONResponse(json)


# Keep this line unchanged
serve()