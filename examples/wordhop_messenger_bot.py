"""
This bot listens to port 5016 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger.bot import Bot
from wordhop import Wordhop
import json

app = Flask(__name__)

ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
WORDHOP_API_KEY = ''
WORDHOP_CLIENT_KEY = ''
bot = Bot(ACCESS_TOKEN)
wordhop = Wordhop(WORDHOP_API_KEY,WORDHOP_CLIENT_KEY,'messenger', ACCESS_TOKEN)

def onChatResponse(self, args):
    print('on_chat_response_response', args)
    channel = args["channel"]
    text = args["text"]
    bot.send_text_message(channel, text)
wordhop.on('chat_response', onChatResponse)

wordhop.start()

@app.route("/", methods=['GET', 'POST'])




def hello():
    def sendIt(channel, text):
        response = bot.send_text_message(channel, text)
        messageData = {'recipient': {'id': channel},'message': {'text': text, 'metadata': "DEVELOPER_DEFINED_METADATA"}}
        wordhop.hopOut(messageData)

    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        print(output)
        
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    j = json.dumps(x)
                    hopInResponse = wordhop.hopIn(x)
                    # If your bot is paused, stop it from replying
                    if hopInResponse.get('paused'):
                        return "Success"
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        if message == 'hi':
                            sendIt(recipient_id, 'Hello there.')
                        elif message == 'help':
                            # let the user know that they are being routed to a human
                            sendIt(recipient_id, 'Hang tight. Let me see what I can do.')
                            # send a Wordhop alert to your slack channel
                            # that the user could use assistance
                            wordhop.assistanceRequested(x);
                        else:
                            # let the user know that the bot does not understand
                            sendIt(recipient_id, 'Huh?')
                            # capture conversational dead-ends.
                            wordhop.logUnknownIntent(x)
                                
                    if x['message'].get('attachment'):
                        bot.send_attachment_url(recipient_id, x['message']['attachment']['type'],
                                                x['message']['attachment']['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5016, debug=True)

