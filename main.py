import ffmpeg, os, nltk
from pytube import YouTube
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import speech_recognition as sr

# Get the url of the video and the word to search for
url = input("Enter the url of the video: ")
word = input("Enter the word you want to search for: ")
yt = YouTube(url)

# Download the video in wemb format
audio_stream = yt.streams.get_by_itag(140)
audio_stream.download(output_path="./audio", filename="audio.mp4")

# Convert the video to wav format
input_file = "./audio/audio.mp4"
output_file = "./audio/output.wav"
ffmpeg.input(input_file).output(output_file, format='wav', loglevel="quiet").run()

# Recognize the speech from the audio file
r = sr.Recognizer()
with sr.WavFile(output_file) as source:
    audio = r.record(source)

recognized_speech = str(r.recognize_azure(audio, key=os.environ.get('SPEECH_KEY'), location=os.environ.get('SPEECH_REGION'), language="en-US", show_all=False,))
try:
    print("Google Speech Recognition thinks you said " + recognized_speech)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Download the nltk data if it doesn't exist
current_user = os.getlogin()
if not os.path.exists("C:\\Users\\" + current_user + "\\AppData\\Roaming\\nltk_data"):
    nltk.download('punkt')

# Tokenize the recognized speech   
tokens = word_tokenize(recognized_speech)
fdist = FreqDist(tokens)

# Print the number of times the word appears in the video
print("The word " + word + " appears " + str(fdist[word]) + " times in the video")

# Delete the audio files
os.remove(input_file)
os.remove(output_file)