import requests
from socketIO_client import SocketIO


class Wordhop:
    def __init__(self, api_key, client_key, platform, *access_token, **kwargs):
        """
            @required:
                api_key
                client_key
                platform
            @optional:
                access_token
                kwargs
        """
        self.headers = {'apikey':api_key,'clientkey':client_key,'platform':platform}
        if access_token:
            self.headers['token'] = access_token[0]
        if kwargs.get('serverRoot'):
            self.serverRoot = kwargs.get('serverRoot')
        else:
            self.serverRoot = 'https://wordhopapi.herokuapp.com'
        if kwargs.get('socketServer'):
            self.socketServer = kwargs.get('socketServer')
        else:
            self.socketServer = 'https://wordhop-socket-server.herokuapp.com'
        if kwargs.get('path'):
            self.path = kwargs.get('path')
        else:
            self.path = '/api/v1/'

        self.apiUrl = self.serverRoot + self.path

        self.platform = platform
        self.clientkey = client_key

        self.start()


    def hopIn(self, x):
        print('hopIn')
        response = requests.post(self.apiUrl + "in",headers=self.headers, json=x)
        result = response.json()
        return result

    def hopOut(self, x):
        print('hopOut')
        response = requests.post(self.apiUrl + "out",headers=self.headers, json=x)
        result = response.json()
        return result
    
    def logUnknownIntent(self, x):
        print('logUnknownIntent')
        response = requests.post(self.apiUrl + "unknown",headers=self.headers, json=x)
        result = response.json()
        return result
    
    def assistanceRequested(self, x):
        print('assistanceRequested')
        response = requests.post(self.apiUrl + "human",headers=self.headers, json=x)
        result = response.json()
        return result
    
    callbacks = None
        
    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}
            
            if event_name not in self.callbacks:
                self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)
        
    def trigger(self, event_name, args):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self, args)

    def start(self):
        
        def setupSocketClient():
            
            def on_socket_set_response(*args):
                socket_id = args[0]
                x = {'socket_id': socket_id, 'clientkey': self.clientkey}
                r = requests.post(self.apiUrl + "update_bot_socket_id",headers=self.headers, json=x)
            
            def on_chat_response_response(*args):
                channel = args[0]["channel"]
                text = args[0]["text"]
                if self.platform == 'messenger':
                    messageData = {'recipient': {'id': channel},'message': {'text': text}}
                else:
                    messageData = {'channel': channel, 'text': text}
                self.hopOut(messageData)
                self.trigger('chat_response', args[0])
            
            
            with SocketIO(self.socketServer) as socketIO:
                socketIO.on('chat response', on_chat_response_response)
                socketIO.on('socket_id_set', on_socket_set_response)
                socketIO.wait()
            
        t = threading.Thread(target=setupSocketClient, args = ())
        t.daemon = True
        t.start()
