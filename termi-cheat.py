#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

CHEATS_DIR = Path(__file__).parent / "cheats"

def show_cheat(command: str, filter: str = None):
    cheat_file = CHEATS_DIR / f"{command}.json"
    if not cheat_file.exists():
        print(f"No cheat sheet for '{command}'. Try: git, docker, etc.")
        return

    with open(cheat_file) as f:
        cheats = json.load(f)

    print(f"\n📖 {command.upper()} CHEATSHEET\n")
    for topic, examples in cheats.items():
        if filter and filter.lower() not in topic.lower():
            continue
        print(f"🔹 {topic}")
        for example in examples:
            print(f"  - {example['cmd']}: {example['desc']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: termi-cheat <command> [--filter=keyword]")
        sys.exit(1)

    command = sys.argv[1]
    filter = next((arg.split("=")[1] for arg in sys.argv if arg.startswith("--filter=")), None)
    show_cheat(command, filter)
