"""bwfsoundlib utils for formatting wave durations to time strings, converting broadcast wave samples to time strings

"""

from datetime import datetime

def samples_to_seconds(samples, rate):
    """Convert audio samples to seconds samples / samplerate."""
    return samples / rate

def sample_seconds_to_time(seconds):
    """Convert the seconds float to a time string."""
    return datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S.%f')

def samples_to_time(samples, samplerate):
    """Convert the broadcast wave  timereference samples to a time string."""
    return sample_seconds_to_time(samples_to_seconds(samples, samplerate))

def format_audio_duration(num_frames, samplerate):
    """Format the audio duration to a time string. Seconds calculated as total_frames / samplerate."""
    return duration_seconds_to_time(num_frames/samplerate)

def duration_seconds_to_time(seconds):
    """Format the audio duration to a time string."""
    return datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S')