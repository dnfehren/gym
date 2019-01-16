
import datetime
import os

import click
from pydub import AudioSegment
from pydub.playback import play


_second = 1000

# activity_count = 6
# circuit_count = 3
# activity_duration = 30
# rest_duration_between_activity = 15
# rest_duration_between_circuits = 30
# transition_seconds = 3


def make_chunk(track, num, duration):
    _chunk_start = num * duration
    _chunk_stop = (num * duration) + duration

    if _chunk_stop > len(track):
        _chunk_start = len(track) - duration
        _chunk_stop = len(track)

    _chunk = track[_chunk_start:_chunk_stop]
    return _chunk


def make_track(fast_audio_loc, slow_audio_loc, output_dir, activity_count, circuit_count, activity_duration=30, rest_duration_between_activity=30, rest_duration_between_circuits=60, transition_seconds=3, rest_audio_loc=None):

    set_active = (activity_duration * _second)
    set_rest = (rest_duration_between_activity * _second) + (transition_seconds * _second)
    circut_rest = (rest_duration_between_circuits * _second) + (transition_seconds * _second)
    fade_duration = transition_seconds * _second

    slow = AudioSegment.from_mp3(slow_audio_loc)
    fast = AudioSegment.from_mp3(fast_audio_loc)

    if rest_audio_loc is not None:
        print('rest track found')
        rest = AudioSegment.from_mp3(rest_audio_loc)
    else:
        rest = AudioSegment.from_mp3(slow_audio_loc)

    interleaved_set_and_rest_chunks = []
    for active_set_num in range(0, activity_count):
        fast_chunk = make_chunk(fast, active_set_num, set_active)
        interleaved_set_and_rest_chunks.append(fast_chunk)

        if active_set_num < activity_count:
            slow_chunk = make_chunk(slow, active_set_num, set_rest)
            interleaved_set_and_rest_chunks.append(slow_chunk)
        else:
            rest_chunk = make_chunk(rest, active_set_num, circut_rest)
            interleaved_set_and_rest_chunks.append(rest_chunk)

    full_track = slow[0 : 3 * fade_duration]
    activity_track = fast[0 : 500]

    for chunk_num, chunk in enumerate(interleaved_set_and_rest_chunks):
        if chunk_num > 0:
            activity_track = activity_track.append(chunk, crossfade=fade_duration)
        else:
            activity_track = activity_track.append(chunk)

    print('activity track made, duration = {} seconds'.format(activity_track.duration_seconds))

    for circuit_num in range(0, circuit_count):
        full_track = full_track + activity_track
    
    print('full circuit track made, duration = {} seconds'.format(full_track.duration_seconds))

    track_loc = os.path.join(output_dir, "sets_{}__circuits_{}__{}.mp3".format(str(activity_count), str(circuit_count), datetime.datetime.now().strftime("%Y%m%d%H%M%S")))

    full_track.export(track_loc, format='mp3')

    return track_loc

def play_track(track_loc):
    cir = AudioSegment.from_file(track_loc, format='mp3')
    play(cir)

@click.command()
@click.option('--fast_track_location', default="/Users/208520/Desktop/gym/Wizard Castle - Winged Mother.mp3")
@click.option('--slow_track_location', default="/Users/208520/Desktop/gym/Ben Prunty - A.C.I.D..mp3")
@click.option('--rest_track_location', default="/Users/208520/Desktop/gym/Chris Zabriskie - Stories About the World That Once Was.mp3")
@click.option('--output_dir', default="/Users/208520/Desktop/gym")
@click.option('--activity_count', default=6)
@click.option('--circuit_count', default=3)
@click.option('--activity_duration', default=30)
@click.option('--activity_rest', default=10)
@click.option('--circuit_rest', default=30)
def cli(fast_track_location, rest_track_location, slow_track_location, output_dir, activity_count, circuit_count, activity_duration, activity_rest, circuit_rest):
    make_track(fast_track_location, slow_track_location, output_dir, activity_count, circuit_count, activity_duration, activity_rest, circuit_rest, rest_audio_loc=rest_track_location)


if __name__ == "__main__":
    cli()
