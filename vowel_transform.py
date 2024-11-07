import numpy as np
import pysptk
import scipy.io as sp
import scipy.signal
import sounddevice as sd
import soundfile as sf


vowels_dict = sp.loadmat('vowels.mat')

sample_rate = int(vowels_dict['fs'][0, 0])
print(sample_rate) #Check sample rate
vowels_audio = vowels_dict['v']

ARC = [0]*len(vowels_audio[0])
pred_err = [0]*len(vowels_audio[0])

for i in range(len(vowels_audio[0])):
    vowels_audio_1 = np.array(vowels_audio[0][i].flatten(), dtype = 'float32')
    sf.write(f'Vowels_data_{i}.wav', vowels_audio_1, sample_rate)

    ARC[i] = pysptk.sptk.lpc(vowels_audio_1, 10)
    pred_err[i] = scipy.signal.lfilter(ARC[i], [1], vowels_audio_1)

run = 1
while(run == 1):

    print("Recording, please pronounce a vowel.")
    duration = 4
    recorded_vowel = sd.rec(int(duration * sample_rate), samplerate = sample_rate, channels=1, dtype = 'float32')
    sd.wait()  
    recorded_vowel = recorded_vowel.flatten() 

    sf.write('Recorded_Vowel.wav', recorded_vowel, sample_rate)

    user_lpc = pysptk.sptk.lpc(recorded_vowel, 10)
    user_pred_error = scipy.signal.lfilter(user_lpc, [1], recorded_vowel)
    select = input('Please enter a vowel\n')
    allowed = 'aeiouyæøå'
    if select.lower() not in allowed:
        print('Entry not a vowel')
        run = 1
    elif select.lower() in allowed:
        keys = {'a' : 0, 'e' : 1, 'i' : 2, 'o' : 3, 'u' : 4, 'y' : 5, 'æ' : 6, 'ø' : 7, 'å' : 8}
        
        transformed_wovel = scipy.signal.lfilter([1], ARC[keys[select.lower()]], user_pred_error)
        sd.play(transformed_wovel, samplerate = sample_rate)
        sd.wait()
        #new_wovel = scipy.signal.lfilter([1], ARC[keys[select.lower()]], pred_err[keys[select.lower()]])
        #sd.play(new_wovel, sample_rate)
        #sd.wait()
        run = 1








