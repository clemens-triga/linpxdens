"""
Command-line interface for the linear pixel density analysis package.

This module provides a simple CLI entry point to run the image analysis
pipeline directly from the terminal.

It allows users to:
- Load an image from a file path
- Execute the full analysis pipeline
- Trigger interactive ROI-based line fitting and evaluation

Usage:
    python -m linpxdens.cli <image_path>
    or (if installed as entry point):
    linpxdens <image_path>
"""

import argparse
from linpxdens import analyze


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Path to image file")
    args = parser.parse_args()

    analyze(args.image)


if __name__ == "__main__":
    main()