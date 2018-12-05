## Advent of Code 2018: Day 4
## https://adventofcode.com/2018/day/4
## Jesse Williams
## Answers: [Part 1]: 77941, [Part 2]:

import re
import datetime

class LogDay(object):
    '''
    An object representing one full day of logs, or equivalently, a guard's behavior for one day.
    daysEntries: [(logTimestamp, logInfo), ...]
    '''
    def __init__(self, daysEntries):
        self.day = daysEntries[1][0].day
        self.month = daysEntries[1][0].month
        self.dateString = '{}/{}'.format(self.month, self.day)
        self.guardID = self._getGuardID(daysEntries)  # the ID of the guard on-duty this day
        self.sleepingMinutes = self._getSleepingMinutes(daysEntries)  # a list of minutes the guard was asleep
        self.timeAsleep = len(self.sleepingMinutes)  # the amount of time the guard was asleep


    def _getGuardID(self, daysEntries):
        pattern = re.compile(r"Guard\s\#(\d+)")
        matches = pattern.match(daysEntries[0][1])
        return int(matches.groups()[0])

    def _getSleepingMinutes(self, daysEntries):
        # Sleep and wake entries will come in order, in pairs, starting at index 1.
        sleepingMinutes = []

        for i in range(len(daysEntries[1::2])):
            sleepMin = daysEntries[2*i+1][0].minute
            wakeMin = daysEntries[2*i+2][0].minute
            sleepingMinutes += list(range(sleepMin, wakeMin))
        return sleepingMinutes


def parseLog(logStr):
    # Takes a log entry in raw string format, e.g. '[1518-11-01 00:00] Guard #N begins shift'

    pattern = re.compile(r'\[(.+)\]\s(.+)')
    matches = pattern.match(logStr)
    (logTimestampStr, logInfo) = matches.groups()

    logTimestamp = datetime.datetime.strptime(logTimestampStr, '%Y-%m-%d %H:%M')

    return (logTimestamp, logInfo)


if __name__ == "__main__":
    # Read input file
    allLogs = []
    with open('day4_input.txt') as f:
        while True:
            logStr = f.readline()
            if logStr == '': break
            allLogs.append(parseLog(logStr))
    allLogs.sort()

    allLogDays, logBatch = [], []
    lastDay = allLogs[0][0].date()  # read first date in log to prime lastDay tracker
    for log in allLogs:

        # Gather a full day of logs and pass them into the LogDay constructor.
        if (log[0].date() == lastDay and not log[0].hour == 23):  # if the day hasn't changed and we haven't skipped to the 23rd hour (start of next day)...
            logBatch.append(log)                                  # add the entry to the day's batch

        else:  # if either the day has changed or the hour is 23, assume we've started the next log day
            if (log[0].date() == lastDay and log[0].hour == 23):      # if it's the same day but the hour has skipped to 23...
                lastDay = log[0].date() + datetime.timedelta(days=1)  # proactively increment to the next day

            else:  # otherwise, we should've skipped to the next day
                lastDay = log[0].date()

            if (len(logBatch) > 1):  # if we don't have at least one sleep period in a day, ignore it
                allLogDays.append(LogDay(logBatch))  # commit batch into LogDay object and add to list
            logBatch = [log]  # clear batch and put in current entry to start new day

    # Fill a dictionary with the time each guard was asleep
    guardSleepTime = {}
    for day in allLogDays:
        #print('Date: {} - ID: {} - Time asleep: {}'.format(day.dateString, day.guardID, day.timeAsleep))

        try:
            guardSleepTime[day.guardID] = guardSleepTime[day.guardID] + day.timeAsleep
        except KeyError:
            guardSleepTime[day.guardID] = day.timeAsleep

    for key in guardSleepTime:
        print('Guard #{} asleep for a total of {} minutes.'.format(key, guardSleepTime[key]))


    sleepiestGuard = list(filter(lambda x:x[1] == max(guardSleepTime.values()), guardSleepTime.items()))[0]

    # Search all LogDay objects, filter only the days when the sleepiest guard was on duty, and accumulate minutes asleep into a 60-array
    sleepiestGuardsMinutes = [0]*60
    for day in allLogDays:
        if (day.guardID == sleepiestGuard[0]):
            for min in day.sleepingMinutes:
                sleepiestGuardsMinutes[min] += 1

    sleepiestGuardsSleepiestMinute = sleepiestGuardsMinutes.index(max(sleepiestGuardsMinutes))

    print('Guard #{} sleeps the most with a total of {} minutes, most frequently during minute {}.'.format(sleepiestGuard[0], sleepiestGuard[1], sleepiestGuardsSleepiestMinute))
