from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

DATA = ROOT_DIR / "data"
PACKAGE = ROOT_DIR / "package"

CONTROLLED_VOC = DATA / "controlled_vocabulary"