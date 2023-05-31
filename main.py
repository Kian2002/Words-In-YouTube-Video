from pytube import YouTube
import speech_recognition as sr
import ffmpeg

# Get the url of the video
url = input("Enter the url of the video: ")
yt = YouTube(url)

# Download the video in wemb format
audio_stream = yt.streams.get_by_itag(251)
audio_stream.download(output_path="./audio", filename="audio.webm")

# Convert the video to wav format
print(yt.title)
input_file = "./audio/audio.webm"
output_file = "./audio/output.wav"
ffmpeg.input(input_file).output(output_file, format='wav').run()

# Recognize the speech
r = sr.Recognizer()
audio_file = "./audio/output.wav"
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

try:
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))