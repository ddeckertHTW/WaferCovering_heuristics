import datetime

def printTimestampDiff(startTimestamp, meassage):
    timestamp_diff = datetime.datetime.now() - startTimestamp
    hours, remainder = divmod(timestamp_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timestamp_diff.microseconds // 1000

    # Formatting the difference
    formatted_diff = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
    print(formatted_diff + meassage)

