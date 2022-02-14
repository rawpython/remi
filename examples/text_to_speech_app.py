#!/usr/bin/env python
import remi.gui as gui
from remi import start, App

"""
This demo allows to test the Text To Speech (TTS) capabilities
of your browser via Remi.
Author: Sammy Pfeiffer
"""

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # We need to get dynamically the available voices
        self.voices_dict = {}
        # Default English_(Great_Britain) voice
        self.selected_voice_id = 78
        self.voices_dropdown = gui.DropDown.new_from_list(["Loading voices list..."],
                                                    width=200, height=20, margin='10px')
        self.container = gui.VBox(width=400)
        self.lbl = gui.Label("Text to say:")
        self.text_input = gui.TextInput(width=300)
        self.lbl_rate = gui.Label("Rate (speed) to say:")
        self.rate_slider = gui.Slider(1.0, min=0.1, max=5.0, step=0.1)
        self.lbl_pitch = gui.Label("Pitch of voice:")
        self.pitch_slider = gui.Slider(1.0, min=0.1, max=2.0, step=0.1)
        self.bt_say = gui.Button("Say")
        self.bt_say.onclick.do(self.on_say)

        self.container.append(self.lbl)
        self.container.append(self.text_input)
        self.container.append(self.lbl_rate)
        self.container.append(self.rate_slider)
        self.container.append(self.lbl_pitch)
        self.container.append(self.pitch_slider)
        self.container.append(self.bt_say)
        self.container.append(self.voices_dropdown, key=99999)

        # returning the root widget
        return self.container

    def idle(self):
        """
        Using the idle function so we can get the available voices when the app opens
        """
        if not self.voices_dict:
            self._get_available_voices()

    def _voices_callback(self, **kwargs):
        # print("_voices_callback args: {}".format(kwargs))
        self.voices_dict = kwargs
        voice_options = kwargs.keys()
        # Show the voice options sorted alphabetically
        voice_options = sorted(voice_options)
        # Sometimes we get an empty list, then do nothing, we will try later again
        if voice_options:
            self.container.remove_child(self.voices_dropdown)
            self.voices_dropdown = gui.DropDown.new_from_list(voice_options,
                                                    width=200, height=20, margin='10px')
            self.voices_dropdown.onchange.do(self._drop_down_changed)
            self.container.append(self.voices_dropdown)
            self.voices_dropdown.select_by_value("English_(Great_Britain)")

    def _drop_down_changed(self, widget, value):
        self.selected_voice_id = int(self.voices_dict[value])
        print("Chosen: {} {}".format(value, self.selected_voice_id))


    # listener function
    def _get_available_voices(self):
        # Here we get the voices and store the one we want
        self.execute_javascript("""
            var synth = window.speechSynthesis;
            voices = synth.getVoices();
            console.log(voices);
            var return_params = {};
            for(voice_id in voices){
                console.log(voices[voice_id].name);
                // Some voices have non-ascii characters and it makes remi crash
                // as the characters have a size bigger than one character
                // and the internal parsing code can't deal with it currently
                name_ascii = voices[voice_id].name.replace(/[\u{0080}-\u{FFFF}]/gu,"");
                return_params[name_ascii] = String(voice_id);
            }
            remi.sendCallbackParam('%(id)s','%(callback_function)s', return_params)""" % {
            'id': str(id(self)),
            'callback_function': '_voices_callback'})

    def on_say(self, widget):
        text = self.text_input.get_text()
        pitch = self.pitch_slider.get_value()
        rate = self.rate_slider.get_value()
        print("Saying: {} at rate {} and pitch {}".format(text, rate, pitch))
        self.execute_javascript(
            """
            var synth = window.speechSynthesis;
            voices = synth.getVoices();
            var utterThis = new SpeechSynthesisUtterance("{}");
            utterThis.pitch = {};
            utterThis.rate = {};
            utterThis.voice = voices[{}];
            synth.speak(utterThis);
            """.format(text, pitch, rate, self.selected_voice_id))

# starts the web server
start(MyApp, address="0.0.0.0", port=9990)
