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
# print(f'Launch Darkly SDK Key: {ld_sdk_key}')  # Debug print statement
feature_flag_key = "dark-mode"
ldclient.set_config(Config(ld_sdk_key))

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