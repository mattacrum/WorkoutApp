import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from scipy.signal import find_peaks
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import read, write
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.clock import Clock
import numpy as np
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

# Supposed to count down 10 seconds before beginning round --broken
class Countdown(Label):
    countdown = NumericProperty(10)

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(countdown=0, duration=self.countdown)
        def finish_callback(animation, timer):
            timer.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

class StrikeCounter(Widget):

    strike_count = NumericProperty(0)
    time_elapsed = StringProperty()
    user = ObjectProperty(None)
    fs = 48000  # Sample rate
    seconds = 130  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file


    def update(self, dt):
        data, fs = sf.read('output.wav')
        data = data[:,0]
        minutes_elapsed = len(data)/fs/60 - (1/6)
        m_e = str(minutes_elapsed)
        temp = m_e.index('.')

        seconds_elapsed = float(m_e[temp:len(m_e)])
        seconds_elapsed = int(seconds_elapsed * 60)
        minutes_elapsed = int(minutes_elapsed)
        self.time_elapsed = 'Elapsed Time: {}:{}'.format(minutes_elapsed, seconds_elapsed)

        scaled_data = []
        data = data[fs*10:len(data)]
        indexes, _ = find_peaks(data, height=0.24, distance=4200.1)

        for item in _['peak_heights']:
            scaled_data.append(item)
        print(scaled_data)
        scaled_data = np.array(scaled_data)
        scaled_data = scaled_data.reshape(1,-1)
        scaled_data = normalize(scaled_data, norm='max')

        plt.plot(scaled_data[0])
        temp = []
        for item in scaled_data[0]:
            if item > 0.18:
                temp.append(item)

        self.strike_count = len(temp)
        print(self.strike_count)



class WorkoutApp(App):
    def build(self):
        countdown = Countdown()
        countdown.start()

        counter = StrikeCounter()
        Clock.schedule_interval(counter.update, 1.0)
        return counter


if __name__ == '__main__':
    WorkoutApp().run()
