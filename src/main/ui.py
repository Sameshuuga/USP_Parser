#!/usr/bin/env python3
import argparse, sys, os, logging
from settings import default_input_dir

logger = logging.getLogger(__name__)


## ------------------------ make-menu ---------------------------------- ##
class Menu:
    """
    Generic numbered menu. Give it a header and a list of (label, value)
    pairs; it prints them, validates input, and returns the chosen value.
    An 'Exit' option is appended automatically.
    """

    def __init__(self, header: str, options: list[tuple[str, object]]):
        self.header = header
        self.options = options

    def prompt(self):
        while True:
            print(f"\n=== {self.header} ===")
            for i, (label, _value) in enumerate(self.options, start=1):
                print(f"{i}. {label}")
            exit_num = len(self.options) + 1
            print(f"{exit_num}. Exit")

            choice = input("Select an option: ").strip()
            if not choice.isdigit():
                print("Please enter a number.")
                continue

            choice = int(choice)
            if choice == exit_num:
                sys.exit()
            elif 1 <= choice <= len(self.options):
                label, value = self.options[choice - 1]
                logger.info(f"Selected: {label}")
                return value
            else:
                print("Invalid choice, try again.")


def make_menu(header: str, items: list, label_fn=str):
    """Convenience wrapper: build a Menu from a plain list of items."""
    options = [(label_fn(item), item) for item in items]
    return Menu(header, options)


##-----------------------------------------------------------------------##
## ------------------------ menus -------------------------------------- ##
def file_menu(directory):
    logger.info("Entering file_menu")
    try:
        entries = sorted(os.listdir(directory))
    except FileNotFoundError:
        logger.error(f"Directory not found: {directory}")
        print(f"Directory not found: {directory}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {directory}")
        print(f"Permission denied: {directory}")
        return None

    files = []
    for f in entries:
        if f.lower().endswith(".pdf"):
            files.append(f)
        else:
            logger.info(f"Rejected: {f}")

    if not files:
        logger.error(f"No files found in {directory}")
        print(f"No files found in {directory}")
        return None

    menu = make_menu(f"Choose Monograph from {directory}:", files)
    selected = menu.prompt()
    monograph = directory / selected
    print(f"You selected: {selected}")
    logger.info(f"{monograph} selected for processing")
    return monograph


def section_menu(monograph: dict):
    menu = make_menu("Select section", [key for key in monograph.keys()])
    return menu.prompt()


##-----------------------------------------------------------------------##
## ------------------------ args --------------------------------------- ##
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="usp-parser",
        description=(
            "Convert USP monograph PDFs into structured section data."
            "Generate a testing documentation templet using the structured data."
        ),
    )
    parser.add_argument(
        "-i",
        "--input",
        default=default_input_dir,
        help=(
            "Specify the location of the directory containing"
            "the pdf files to be processed (default: %(default)s)"
        ),
    )
    parser.add_argument("-b", "--batch", help=("Batch process all files in "))

    return parser


##-----------------------------------------------------------------------##
