from typing import Callable

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
def _get_number(prompt: str, convert: Callable, minimum: float,
                allow_equal: bool, kind: str) -> float:
    while True:
        try:
            value = convert(input(prompt))
        except ValueError:
            print(f"Please enter a valid {kind}.")
            continue
        if value < minimum or (value == minimum and not allow_equal):
            print("Please enter a number greater than zero." if not allow_equal
                  else "Please enter zero or a positive number.")
            continue
        return value
def get_non_negative_float(prompt: str) -> float:
    return _get_number(prompt, float, 0, True, "number, e.g. 2.5")
def get_non_negative_int(prompt: str) -> int:
    return _get_number(prompt, int, 0, True, "whole number")
def get_positive_int(prompt: str) -> int:
    return _get_number(prompt, int, 0, False, "whole number")