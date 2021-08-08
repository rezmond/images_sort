from typeguard import typechecked

REPORT_LINE_LENGTH = 80


@typechecked
def report_line(
        text: str, value: int, lenght: int = REPORT_LINE_LENGTH) -> str:
    final_text = f'{text}:'
    final_value = str(value)
    pad_length = lenght - len(final_text) - len(final_value)

    return f'{final_text}{" " * pad_length}{final_value}'


@typechecked
def report_devider(delimiter="=", lenght: int = REPORT_LINE_LENGTH) -> str:
    return delimiter * lenght
