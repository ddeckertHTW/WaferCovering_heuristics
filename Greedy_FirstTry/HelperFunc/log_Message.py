import datetime

def logMessage(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Truncate microseconds to milliseconds
    print(f'{timestamp} - {message}')

def getLogMessageString(message, startTimestamp = None):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Truncate microseconds to milliseconds
    testvar = datetime.datetime.now() - startTimestamp if startTimestamp is not None else None
    return({'message': message,
            'timeSinceStart': (datetime.datetime.now() - startTimestamp) if startTimestamp else None, 
            'timestamp': timestamp,  
            })


def printTimestampDiff(startTimestamp, meassage):
    timestamp_diff = datetime.datetime.now() - startTimestamp
    hours, remainder = divmod(timestamp_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timestamp_diff.microseconds // 1000

    # Formatting the difference
    formatted_diff = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
    print(formatted_diff + meassage)

def fornatTimestampDiff(timestamp_diff):
    hours, remainder = divmod(timestamp_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timestamp_diff.microseconds // 1000

    # Formatting the difference
    formatted_diff = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
    return formatted_diff

