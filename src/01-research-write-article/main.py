"""A Multi-Agent system for Research and Write an article about a topic."""

from crew import ResearchAndWriterCrew
from dotenv import load_dotenv

import argparse


def argument_parser() -> argparse.ArgumentParser:
    """Parse incoming CLI arguments."""
    args = argparse.ArgumentParser()
    args.add_argument("--topic", required=True, help="Research topic.")
    return args.parse_args()


if __name__ == "__main__":
    # Parse incoming arguments
    args = argument_parser()

    # Load environment file
    load_dotenv()

    # Instatiate crew
    ResearchAndWriterCrew().run(args.topic)
