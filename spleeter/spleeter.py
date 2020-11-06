from spleeter.separator import Separator

track_path = 'giant_steps.wav'

separator = Separator('spleeter:5stems')

separator.separate_to_file(track_path)