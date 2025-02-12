"""A Multi-Agent System for Customer Outreach Campaign."""

from crew import CustomerOutreach
from dotenv import load_dotenv

import argparse


def argument_parser() -> argparse.ArgumentParser:
    """Parse incoming CLI arguments."""
    args = argparse.ArgumentParser()
    args.add_argument("--verbose", action=argparse.BooleanOptionalAction,
                      default=False, help="Enable verbose mode.")
    args.add_argument("--lead_name",
                      required=True,
                      help="Company name")
    args.add_argument("--industry",
                      required=True,
                      help="Industry of the campaign.")
    args.add_argument("--maker",
                      required=True,
                      help="Name of the key decision maker.")
    args.add_argument("--position",
                      required=True,
                      help="Position of the key decision maker.")
    args.add_argument("--milestone",
                      required=True,
                      help="Milestone to achieve.")
    return args.parse_args()


if __name__ == "__main__":
    # Parse incoming arguments
    args = argument_parser()

    # Load environment file
    load_dotenv()

    # Build inputs dictionary
    inputs = {
        "lead_name": args.lead_name,
        "industry": args.industry,
        "key_decision_maker": args.maker,
        "position": args.position,
        "milestone": args.milestone,
    }

    try:
        # Instatiate crew
        result = CustomerOutreach(args.verbose).run(inputs=inputs)
        print(f"Result: {result}")
    except KeyboardInterrupt:
        print("CTRL + C pressed. Ending the execution...")