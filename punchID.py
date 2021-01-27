import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import soundfile as sf
import numpy as np
import sys
from sklearn.preprocessing import normalize
np.set_printoptions(threshold=sys.maxsize)

def readPunches(fileName):
    # Read audio file using soundfile
    data, fs = sf.read('output_~101.wav')

    # Total minutes - 10s
    minutes_elapsed = len(data)/fs/60 - (1/6)
    m_e = str(minutes_elapsed)
    temp = m_e.index('.')

    seconds_elapsed = float(m_e[temp:len(m_e)])
    seconds_elapsed = int(seconds_elapsed * 60)

    print('Length of Round: %d minutes and %d seconds' % (int(minutes_elapsed), seconds_elapsed))

    # Remove data that is clearly not a strike
    # by making an array of peaks
    data = data[:,0]

    scaled_data = []
    data = data[fs*5:len(data)]

    indexes, _ = find_peaks(data, height=0.24, distance=4200.1)
    plt.plot(_['peak_heights'])

    for item in _['peak_heights']:
        scaled_data.append(item)

    scaled_data = np.array(scaled_data)
    scaled_data = scaled_data.reshape(1,-1)
    scaled_data = normalize(scaled_data, norm='max')

    # Find strikes by removing values under 18% of the max
    temp = []
    for item in scaled_data[0]:
        if item > 0.18:
            temp.append(item)

    strike_total = len(temp)
    print('You threw %d punches' % strike_total)