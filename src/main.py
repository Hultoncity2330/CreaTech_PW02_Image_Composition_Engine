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


def get_next_output_path(output_dir: Path, base_name: str = "output", suffix: str = ".png") -> Path:
    """Return the next available numbered output path."""
    first_path = output_dir / f"{base_name}{suffix}"

    if not first_path.exists():
        return first_path

    index = 1
    while True:
        candidate = output_dir / f"{base_name}{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def main():
    """Run the image composition engine."""

    args = parse_args()

    try:
        config_path = Path(args.config)

        if not config_path.is_absolute():
            config_path = SRC_DIR / config_path

        config = load_config(str(config_path))
        result = BlendEngine().run_pipeline(config)

        OUTPUT_DIR.mkdir(exist_ok=True)

        if args.output:
            output_path = Path(args.output)
            if not output_path.is_absolute():
                output_path = OUTPUT_DIR / output_path
        else:
            output_path = get_next_output_path(OUTPUT_DIR)

        image_io.save_image(result, str(output_path))
    
    except (ValueError, KeyError, FileNotFoundError, OSError) as error:
        print(f"Error : {error}", file = sys.stderr)
        return 1

    print(f"Image saved: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

