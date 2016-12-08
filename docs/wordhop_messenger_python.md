# [Wordhop](https://www.wordhop.io) - Monitor and Optimize Your Conversational Experience
## For Chatbots Built in Python

With Wordhop you can sync up your Python-based Chatbot to Slack, so you can retain your users without ever leaving Slack.  Wordhop monitors your Chatbot for friction in your conversational experience and alerts you on Slack in real-time. Simply add Wordhop to Slack and then drop in a couple of lines of code into your Chatbot.  Wordhop integrates in minutes, not days, and begins working immediately.  From Slack, you can pause and take over your bot, then hand the conversation back to your bot.  Actionable analytics also show you and your Slack team where you can optimize your conversational experience and measure results. 

### What you can do with Wordhop:
* [See Key Features](https://developer.wordhop.io)
* [Watch a Demo](https://www.youtube.com/watch?v=TAcwr3s9l4o)

### What you need to get started:
* [A Slack Account](http://www.slack.com)
* [Wordhop for Slack](https://slack.com/oauth/authorize?scope=users:read,users:read.email,commands,chat:write:bot,channels:read,channels:write,bot&client_id=23850726983.39760486257)
* [A Chatbot built in Python](../examples/messenger/README.md)

### Installation

```bash
pip install wordhop
```


### Usage

```python
from wordhop import Wordhop

wordhop = Wordhop(WORDHOP_API_KEY,WORDHOP_CLIENT_KEY,'messenger', ACCESS_TOKEN)
```

__Note__: From Facebook regarding User IDs

> These ids are page-scoped. These ids differ from those returned from Facebook Login apps which are app-scoped. You must use ids retrieved from a Messenger integration for this page in order to function properly.

> If `app_secret` is initialized, an app_secret_proof will be generated and send with every request.
> Appsecret Proofs helps further secure your client access tokens. You can find out more on the [Facebook Docs](https://developers.facebook.com/docs/graph-api/securing-requests#appsecret_proof)


##### Tracking received messages:

When Messenger calls your receiving webhook, you'll need to log the data with Wordhop. 
__Note__: Wordhop can pause your bot so that it doesn't auto response while a human has taken over. The server response from your `hopIn` request will pass the `paused` state. Use that to stop your bot from responding to an incoming message. Here is an example:

```python
hopInResponse = wordhop.hopIn(messageData)
# If your bot is paused, stop it from replying
if hopInResponse.get('paused'):
    return "Success"
    ...
```

##### Tracking sent messages:

Each time your bot sends a message, make sure to log that with Wordhop in the request's callback. Here is an example:
```python
def sendIt(channel, text):
    messageData = {'recipient': {'id': channel},'message': {'text': text}}
    wordhop.hopOut(messageData)
    bot.send_text_message(channel, text) # <= example of bot sending reply
    ...
```

##### Human Take Over:

To enable the ability to have a human take over your bot, add the following code:

```python
# Handle forwarding the messages sent by a human through your bot
def onChatResponse(self, args):
    channel = args["channel"]
    text = args["text"]
    bot.send_text_message(channel, text) # <= example of bot sending message
    
wordhop.on('chat_response', onChatResponse)
```
##### Log Unknown Intents:

Find the spot in your code your bot processes incoming messages it does not understand. You may have some outgoing fallback message there (i.e. "Oops I didn't get that!"). Within that block of code, call to `wordhop.logUnkownIntent` to capture these conversational ‘dead-ends’. Here's an example:

```python
# let the user know that the bot does not understand
sendIt(recipient_id, 'Huh?')
# capture conversational dead-ends.
wordhop.logUnknownIntent(messageData) 
```
##### Dial 0 to Speak With a Live Human Being:

Wordhop can trigger alerts to suggest when a human should take over for your Chatbot. To enable this, create an intent such as when a customer explicitly requests live assistance, and then include the following line of code where your bot listens for this intent:

```python
# match an intent to talk to a real human
if message == 'help':
    # let the user know that they are being routed to a human
    sendIt(recipient_id, 'Hang tight. Let me see what I can do.')
    # send a Wordhop alert to your slack channel
    # that the user could use assistance
    wordhop.assistanceRequested(messageData);
```

Go back to Slack and wait for alerts. That's it! 
[Be sure to check out our example.](../examples/messenger/README.md)


### Looking for something we don't yet support?  
* [Join our mailing list and we'll notifiy you](https://www.wordhop.io/contact.html)
* [Contact Support](mailto:support@wordhop.io)
