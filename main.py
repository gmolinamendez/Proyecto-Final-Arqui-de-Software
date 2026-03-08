from flask import Flask, render_template


app = Flask(__name__)


from APIs.Users import *  # noqa: E402,F401,F403
from APIs.Events import *  # noqa: E402,F401,F403
from APIs.Persons import *  # noqa: E402,F401,F403
from APIs.Attendees import *  # noqa: E402,F401,F403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
