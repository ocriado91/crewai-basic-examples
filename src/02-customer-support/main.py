"""A Multi-Agent system for Customer Support"""

from crew import CustomerSupport
from dotenv import load_dotenv

import argparse


def argument_parser() -> argparse.ArgumentParser:
    """Parse incoming CLI arguments."""
    args = argparse.ArgumentParser()
    args.add_argument("--verbose", action=argparse.BooleanOptionalAction,
                      default=False, help="Enable verbose mode.")
    args.add_argument("--customer",
                      required=True,
                      help="Company name.")
    args.add_argument("--person",
                      required=True,
                      help="Person name.")
    args.add_argument("--inquiry",
                      required=True,
                      help="Inquiry of the customer.")
    return args.parse_args()


if __name__ == "__main__":
    # Parse incoming arguments
    args = argument_parser()

    # Load environment file
    load_dotenv()

    # Build inputs dictionary
    inputs = {
        "customer": args.customer,
        "person": args.person,
        "inquiry": args.inquiry,
    }

    try:
        # Instatiate crew
        CustomerSupport(args.verbose).run(inputs=inputs)
    except KeyboardInterrupt:
        print("CTRL + C pressed. Ending the execution...")
