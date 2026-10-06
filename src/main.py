import argparse
import sys
import json

import image_io
from engine import BlendEngine


def parse_args():
    p = argparse.ArgumentParser(description="Pipeline de blending piloté par JSON")
    p.add_argument("config", help="fichier JSON du pipeline")
    p.add_argument("-o", "--output", default=None, help="remplace 'output' du JSON")
    return p.parse_args()


def main():
    args = parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    engine = BlendEngine()
    try:
        result = engine.run_pipeline(config)  # + apply_filter=... quand les filtres existent
    except (ValueError, KeyError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1

    output = args.output or config.get("output", "output.png")
    image_io.save_image(output, result)
    print(f"Image enregistrée : {output}")
    return 0