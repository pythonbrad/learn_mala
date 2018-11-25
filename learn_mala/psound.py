import pyaudio
import wave
import _thread

_playing = False

def play(filename, rep):
	stop()
	global _playing
	_playing = True
	_thread.start_new(_player, (filename,rep,))

def _player(filename, rep):
	global _playing
	global soundir
	try:
		chunk = 1024
		p = pyaudio.PyAudio()
		wf = wave.open('sound/'+rep+'/'+filename+".wav", 'rb')
		stream = p.open(
			format = p.get_format_from_width(wf.getsampwidth()),
			channels = wf.getnchannels(),
			rate = wf.getframerate(),
			output = True)
		data = wf.readframes(chunk)
		while data != b'':
			stream.write(data)
			data = wf.readframes(chunk)
			if not _playing:
				break
		stream.close()
		p.terminate()
	except Exception as error:
		print("Sound '%s.wav' error: %s"%(filename.lower(),error))
	_playing = False

def stop():
	global _playing
	_playing = False

