from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]

CONFIG_PATH = PACKAGE_ROOT / "config" / "projects.json"
DATA_PATH = PROJECT_ROOT / "data"
PLACEHOLDER_PATH = DATA_PATH / "placeholder.png"
UI_PATH = PACKAGE_ROOT / "ui" / "view" / "interface.ui"

print("PACKAGE_ROOT:", PACKAGE_ROOT)
print("PROJECT_ROOT:", PROJECT_ROOT)
print("CONFIG_PATH:", CONFIG_PATH)