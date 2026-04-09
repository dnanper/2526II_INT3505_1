from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from Buoi7.database import seed_database, show_summary


if __name__ == "__main__":
    seed_database()
    show_summary()
