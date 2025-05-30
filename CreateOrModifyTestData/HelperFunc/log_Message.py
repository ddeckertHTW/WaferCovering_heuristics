import datetime

def logMessage(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Truncate microseconds to milliseconds
    print(f'{timestamp} - {message}')