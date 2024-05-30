import sys


def progress_bar(finish_tasks_number, tasks_number):
    """
    :param finish_tasks_number: int,
    :param tasks_number: int,
    :return:
    """
    percentage = round(finish_tasks_number / tasks_number * 100)
    print("\rdownloading: {}%: ".format(percentage), "▓" * (percentage // 2), end="")
    sys.stdout.flush()
