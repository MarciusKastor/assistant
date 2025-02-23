#!/usr/bin/env python3
import json
from modules.database import init_db
from modules.webapp import run_app

def main():
    with open("config/config.json", "r") as f:
        config = json.load(f)
    db_conn = init_db()
    run_app()

if __name__ == "__main__":
    main()
