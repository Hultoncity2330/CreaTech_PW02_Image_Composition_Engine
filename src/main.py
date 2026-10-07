import argparse
import sys
from pathlib import Path

import image_io
from config import load_config
from engine import BlendEngine


SRC_DIR = Path(__file__).parent
OUTPUT_DIR = SRC_DIR / "output"


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description = "Run the image composition pipeline from a JSON configuration.")
    parser.add_argument("config", nargs = "?", default = "config.json", help = "Path to the JSON configuration file.")
    parser.add_argument("-o", "--output", default = None, help = "Override the output filename.")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        config_path = Path(args.config)

        if not config_path.is_absolute():
            config_path = BASE_DIR / config_path

        config = load_config(str(config_path))
        result = BlendEngine().run_pipeline(config)

        output = args.output or config.get("output", "output.png")
        output_path = Path(output)

        if not output_path.is_absolute():
            output_path = OUTPUT_DIR / output_path

        OUTPUT_DIR.mkdir(exist_ok = True)

        image_io.save_image(result, str(output_path))
    
    except (ValueError, KeyError, FileNotFoundError, OSError) as e:
        print(f"Error : {e}", file = sys.stderr)
        return 1

    print(f"Image saved: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
