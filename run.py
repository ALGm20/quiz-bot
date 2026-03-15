import threading, os, logging
logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)

def run_dash():
    from dashboard import app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8090)), debug=False, use_reloader=False)

def run_bot():
    from bot import main
    main()

if __name__ == "__main__":
    threading.Thread(target=run_dash, daemon=True).start()
    run_bot()
