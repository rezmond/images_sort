import time
import click


def the_same_line(line):
    return f'{line}'


def report_to_str(report):
    if index % 19 != 0:
        return the_same_line(
            f'{report} --> far far away'
        )

    return the_same_line(report)


index = 0
prev = ''


def item_show_func(report):
    if report:
        return report_to_str(report)

    return None


lng = 100

moved_reports = range(lng)

with click.progressbar(
    moved_reports,
    length=lng,
    bar_template='[%(bar)s] %(info)s\n',
) as gen:
    for x in gen:
        index += 1
        print(f'\n\033[K<<<{item_show_func(x)}>>>\033[2A')
        time.sleep(0.07)

print()
print()
