from __future__ import print_function
from __future__ import unicode_literals
from wordhop import Wordhop
from rtmbot.core import Plugin, Job
from slackclient import SlackClient

WORDHOP_API_KEY = ""
WORDHOP_CLIENT_KEY = ""
wordhop = Wordhop(WORDHOP_API_KEY,WORDHOP_CLIENT_KEY,'slack')


class WordhopListener():
    def __init__(self, plugin):
        def onChatResponse(self, args):
            print('on_chat_response_response', args)
            channel = args["channel"]
            text = args["text"]
            plugin.outputs.append([channel, text])
        
        wordhop.on('chat_response', onChatResponse)
        
        def onChannelUpdate(self, args):
            print('on_channel_update', args)
        
        wordhop.on('channel_update', onChannelUpdate)
        wordhop.start()



class WordhopPlugin(Plugin):
    
    def process_message(self, data):

        hopInResponse = wordhop.hopIn(data)
        # If your bot is paused, stop it from replying
        if hopInResponse.get('paused'):
           return "Success"
        
        def sendIt(channel, text):
            self.outputs.append([channel, text])
            wordhop.hopOut({'channel':channel, 'text':text})
        
        channel = data['channel']
        text = data['text']
        
        if (text == 'hi' or text == 'hello'):
            sendIt(channel, 'Hello there.')
        elif (text == "help" or text == "operator"):
            # send a Wordhop alert to your slack channel
            # that the user could use assistance
            wordhop.assistanceRequested(data);
            # let the user know that they are being routed to a human
            sendIt(channel, 'Hang tight. Let me see what I can do.')

        # otherwise log an unknown intent with Wordhop
        else:
            # capture conversational 'dead-ends'.
            wordhop.logUnknownIntent(data)
            # let the user know that the bot does not understand
            sendIt(channel, 'Huh?')
                
    def register_jobs(self):
        WordhopListener(self)
