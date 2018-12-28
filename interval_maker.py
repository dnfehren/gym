from pydub import AudioSegment
from pydub.playback import play

slow = AudioSegment.from_mp3("Chris Zabriskie - Stories About the World That Once Was.mp3")
fast = AudioSegment.from_mp3("Wizard Castle - Winged Mother.mp3")

_second = 1000

active_sets = 6
set_active = 30 * _second + (3 * _second)
set_rest = 30 * _second + (3 * _second)
circut_rest = 90 * _second + (3 * _second)
set_rest_count = 5
total_rest_count = set_rest_count + 1

fade = 3 * _second

def make_chunk(track, num, duration):
    _chunk_start = num * duration
    _chunk_stop = (num * duration) + duration

    if _chunk_stop > len(track):
        _chunk_start = len(track) - duration
        _chunk_stop = len(track)

    _chunk = track[_chunk_start:_chunk_stop]
    return _chunk

interleaved_circuit_chunks = []
for active_set_num in range(0, active_sets + 1):
    fast_chunk = make_chunk(fast, active_set_num, set_active)
    interleaved_circuit_chunks.append(fast_chunk)

    if active_set_num < active_set_num + 1:
        slow_chunk = make_chunk(slow, active_set_num, set_rest)
        interleaved_circuit_chunks.append(slow_chunk)
    else:
        rest_chunk = make_chunk(slow, active_set_num, circut_rest)
        interleaved_circuit_chunks.append(rest_chunk)

full_track = slow[0 : 2 * fade]
for chunk in interleaved_circuit_chunks:
    full_track = full_track.append(chunk, crossfade=fade)

full_track.export('cir2.mp3', format='mp3')

cir = AudioSegment.from_file('cir2.mp3', format='mp3')
play(cir)