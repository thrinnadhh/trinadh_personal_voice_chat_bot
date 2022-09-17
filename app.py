##Getting the dependencies
import os
import openai
#importing the python text to speech conversation library
import pyttsx3
#importing the speech recognisation library
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()
openai.api_key=os.getenv('OPENAI_API_KEY')

##initialization of the python text to speech conversation storing it in engine variable
engine=pyttsx3.init()
r=sr.Recognizer()

##knowing the mics available.
print(sr.Microphone.list_microphone_names())

#assigning the mic for the input.
mic=sr.Microphone(device_index=0)

#for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

##initialzing the conversation with an empty string first.
conversation=""
user_name='Trinadh'

while True:
    with mic as source:
        print('\nlistening.....speak clearly into the mic.....')
        #inorder to adjust the background noise we need to use the adjust_ambient_noise
        r.adjust_for_ambient_noise(source,duration=0.4)
        audio=r.listen(source)
    print('no longer listening.\n')
    try:
        ##google library to recognise speech after all the audio has been sent and processed.
        user_input=r.recognize_google(audio)
    except:
        continue
    prompt=user_name+':'+user_input+'\nAva:'
    conversation+=prompt
    response=openai.Completion.create(engine='text-davinci-001',prompt=conversation,max_tokens=100)
    response_str=response['choices'][0]['text'].replace('\n',"")
    ##To remove the unwanted conversation
    response_str=response_str.split(user_name+":",1)[0].split('bot: ',1)[0]


    conversation+=response_str+"\n"
    print(response_str)

##To spell the conversation
    engine.say(response_str)
    engine.runAndWait()
