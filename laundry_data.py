import csv
from operator import itemgetter
from statistics import mean

import matplotlib.pyplot as plt


def sort_by_key(d: dict):
    return {key: value for key, value in sorted(
        d.items(), key=itemgetter(0))}


def get_hourly_mean(data, days: list):
    hourly_mean = [[] for h in range(24)]

    for hour in range(24):
        hour_data = []

        for day in days:
            for minute in range(60):
                for data_point in data[day][hour][minute]:
                    hour_data.append(data_point)
        hourly_mean[hour] = mean(hour_data)

    return hourly_mean


def create_figure(data, name: str):
    fig, ax = plt.subplots()

    ax.plot(list(range(24)), get_hourly_mean(data, weekdays), label='weekday')
    ax.plot(list(range(24)), get_hourly_mean(data, weekends), label='weekend')

    ax.legend()
    fig.savefig(name + '.png', dpi=157.35)


if __name__ == '__main__':
    weekdays = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday']
    weekends = [
        'Saturday',
        'Sunday']

    washer_data = {}
    dryer_data = {}

    with open('laundry.csv', mode='r') as file:
        reader = csv.DictReader(file)

        for r in reader:
            if r['weekday'] not in washer_data:
                washer_data[r['weekday']] = [
                    [[] for m in range(60)] for h in range(24)]
            if r['weekday'] not in dryer_data:
                dryer_data[r['weekday']] = [
                    [[] for m in range(60)] for h in range(24)]

            hour, minute = (int(_) for _ in r['time'].split(':'))

            washer_data[r['weekday']][hour][minute].append(int(r['washers']))
            dryer_data[r['weekday']][hour][minute].append(int(r['dryers']))

    create_figure(washer_data, 'wahsers')
    create_figure(dryer_data, 'dryers')