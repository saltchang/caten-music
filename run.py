# run.py

from caten_music import CreateApp

app = CreateApp().main()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
