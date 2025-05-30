import datetime

def convert_TimestampDiff_to_string(startTimestamp):
    hours, remainder = divmod(startTimestamp.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = startTimestamp.microseconds // 1000

    # Formatting the difference
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"

