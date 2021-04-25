def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    placeholder = '=' * filled_len + '-' * (bar_len - filled_len)

    print(f'[{placeholder}] {percents}% ...{status}\r', end='')
