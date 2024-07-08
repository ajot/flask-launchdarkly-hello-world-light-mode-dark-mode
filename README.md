# Flask LaunchDarkly Hello World: Light Mode/Dark Mode

This is a simple Flask application that demonstrates how to use LaunchDarkly to switch between dark mode and light mode based on a feature flag. The application uses the LaunchDarkly Python SDK to evaluate the feature flag for a given user context.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:
- A LaunchDarkly account
- Python 3.x installed
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/flask-launchdarkly-hello-world-light-mode-dark-mode.git
    cd flask-launchdarkly-hello-world-light-mode-dark-mode
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install flask launchdarkly-server-sdk python-dotenv
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root directory and add your LaunchDarkly SDK key:

    **`.env`**:

    ```sh
    LAUNCHDARKLY_API_KEY=your_launchdarkly_sdk_key
    FLASK_RUN_PORT=3000
    ```

### HTML Templates

Create a `templates` directory and add the following HTML files:

**`templates/base.html`**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body class="{{ 'dark-mode' if dark_mode else 'light-mode' }}">
    {% block content %}{% endblock %}
</body>
</html>
```

**`templates/index.html`**:

```html
{% extends "base.html" %}

{% block content %}
<h1>Welcome to the Flask App</h1>
<p>The current mode is {{ 'Dark' if dark_mode else 'Light' }} Mode.</p>
{% endblock %}
```

### CSS for Dark Mode and Light Mode

Create a `static` directory and add a CSS file:

**`static/style.css`**:

```css
body.light-mode {
    background-color: white;
    color: black;
}

body.dark-mode {
    background-color: black;
    color: white;
}
```

### Running the Application

1. **Run the Flask application:**

    ```sh
    flask run
    ```

2. **Open your browser and navigate to:**

    ```
    http://localhost:3000/?email=hello@example.com
    ```

    You should see the page display the current mode (Dark or Light) based on the feature flag value in LaunchDarkly.

### Debugging

- If you encounter issues, check the terminal output for debug statements.
- Ensure that the `LAUNCHDARKLY_API_KEY` environment variable is set correctly and that your LaunchDarkly account has the correct feature flag configuration.

## Code Overview

### `app.py`

Here's a quick look at the main Flask application code:

```python
import os
from flask import Flask, request, render_template
import ldclient
from ldclient.config import Config
from ldclient.context import Context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize LaunchDarkly client
ld_sdk_key = os.getenv("LAUNCHDARKLY_API_KEY")
print(f'Launch Darkly SDK Key: {ld_sdk_key}')  # Debug print statement
feature_flag_key = "dark-mode"
ldclient.set_config(Config(ld_sdk_key))

print(f"LaunchDarkly SDK Key: {ld_sdk_key}")  # Debug print statement

@app.route("/")
def index():
    email = request.args.get('email', 'default@example.com')
    
    # Specify the user and email to LaunchDarkly as a Context
    context = Context.builder(email).kind('user').set("email", email).build()

    # Obtain the feature flag evaluated value
    dark_mode = ldclient.get().variation(feature_flag_key, context, False)
    print(f"Email: {email}, Dark Mode: {dark_mode}")  # Debug print to verify flag value
    
    return render_template("index.html", dark_mode=dark_mode)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
```

## Conclusion

This demo shows how to set up a simple Flask application that dynamically switches between dark mode and light mode based on a feature flag from LaunchDarkly. It’s a great way to start using feature flags to control the user experience dynamically in your applications.