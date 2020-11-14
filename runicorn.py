from uvicorn import run
import sys

if __name__ == "__main__":
    run(sys.argv[1], host="0.0.0.0", port=8000, reload=True)
