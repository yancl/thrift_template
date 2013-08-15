from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server.TServer import TThreadPoolServer
from thrift.server.TNonblockingServer import TNonblockingServer


def post_prepare(self):
    print 'running on port:',self.serverTransport.port


def threadpool_prepare(self):
    """Start a fixed number of worker threads and put client into a queue"""
    for i in range(self.threads):
      try:
        t = threading.Thread(target=self.serveThread)
        t.setDaemon(self.daemon)
        t.start()
      except Exception as x:
        logging.exception(x)

    # Pump the socket for clients
    self.serverTransport.listen()

def threadpool_serve(self):
    self.prepare()

    #do something after address binding
    #for example, register self to nameservice
    self.post_prepare()

    while True:
      try:
        client = self.serverTransport.accept()
        self.clients.put(client)
      except Exception as x:
        logging.exception(x)


def nonblock_serve(self):
    """Serve requests.
    
    Serve requests forever, or until stop() is called.
    """
    self._stop = False
    self.prepare()
    self.post_prepare()
    while not self._stop:
        self.handle()

TThreadPoolServer.post_prepare = post_prepare
TThreadPoolServer.prepare = threadpool_prepare
TThreadPoolServer.serve =  threadpool_serve


TNonblockingServer.post_prepare = post_prepare
TNonblockingServer.serve =  nonblock_serve

def thread_pool_server_runner(app, global_conf, **kwargs):
    for name in ['port', 'pool_size']:
        if name in kwargs:
            kwargs[name] = int(kwargs[name])
    pool_size = kwargs.pop('pool_size')
    host = kwargs.pop('host', '0.0.0.0')
    transport = TSocket.TServerSocket(**kwargs)
    transport.host = host
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TThreadPoolServer(app, transport, tfactory, pfactory)
    if pool_size:
        server.threads = pool_size
    server.serve()


def nonblock_server_runner(app, global_conf, **kwargs):
    for name in ['port']:
        if name in kwargs:
            kwargs[name] = int(kwargs[name])
    host = kwargs.pop('host', '0.0.0.0')
    transport = TSocket.TServerSocket(**kwargs)
    transport.host = host
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TNonblockingServer(app, transport, pfactory, pfactory)
    server.serve()
