# 代码生成时间: 2025-09-24 15:54:49
# responsive_layout_app.py

"""
This Quart application demonstrates a responsive layout design.
It serves a simple HTML template that adjusts its layout based on the screen size.
"""

from quart import Quart, render_template

app = Quart(__name__)

# Define the HTML template to be served
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Layout</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .content {
            text-align: center;
        }
        @media (max-width: 600px) {
            .content {
                font-size: 14px;
            }
        }
        @media (min-width: 601px) and (max-width: 1200px) {
            .content {
                font-size: 18px;
            }
        }
        @media (min-width: 1201px) {
            .content {
                font-size: 22px;
            }
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Welcome to the Responsive Layout!</h1>
        <p>This layout adjusts based on your screen size.</p>
    </div>
</body>
</html>
"""

@app.route("/")
async def home():
    # Respond with the HTML template
    return await render_template(HTML_TEMPLATE)

if __name__ == "__main__":
    # Run the Quart application
    app.run()
