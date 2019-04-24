# run.py

import os

from caten_worship import create_app

app = create_app(os.environ.get("APP_SETTING"))

if __name__ == "__main__":
    app.run()
