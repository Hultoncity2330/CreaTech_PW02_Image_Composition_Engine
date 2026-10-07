import argparse
import sys
from pathlib import Path

import image_io
from config import load_config
from engine import BlendEngine

OUTPUT_DIR = Path(__file__).parent / "output"

def parse_args():
    p = argparse.ArgumentParser(description="Pipeline de blending piloté par JSON")
    p.add_argument("config", nargs="?", default="config.json", help="fichier JSON du pipeline")
    p.add_argument("-o", "--output", default=None, help="remplace 'output' du JSON")
    return p.parse_args()


def main():
    args = parse_args()

    try:
        config = load_config(args.config)
        result = BlendEngine().run_pipeline(config)
    except (ValueError, KeyError, FileNotFoundError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1

    output = args.output or config.get("output", "output.png")
    output_path = OUTPUT_DIR / output   # si 'output' est un chemin absolu, il est conservé tel quel
    OUTPUT_DIR.mkdir(exist_ok=True)     # crée le dossier s'il n'existe pas
    image_io.save_image(result, str(output_path))
    print(f"Image enregistrée : {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())