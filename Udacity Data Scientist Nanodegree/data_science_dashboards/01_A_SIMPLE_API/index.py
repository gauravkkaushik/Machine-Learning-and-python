from fasthtml.common import *

# 1. Setup the app
app = FastHTML()

# 2. Define the route
@app.route('/')
def get():
    # FastHTML automatically wraps strings in a <div> or basic HTML structure
    return Titled("Home Page", P("Hello World!"))

# 3. Run the server
if __name__ == "__main__":
    serve()