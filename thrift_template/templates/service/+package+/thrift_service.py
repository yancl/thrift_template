from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server.TServer import TThreadPoolServer
from thrift.server.TNonblockingServer import TNonblockingServer


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
    while not self._stop:
        self.handle()

TThreadPoolServer.prepare = threadpool_prepare
TThreadPoolServer.serve =  threadpool_serve
TNonblockingServer.serve =  nonblock_serve


def post_prepare(app, global_conf, **kwargs):
    print 'global_conf:', global_conf
    print 'kwargs:', kwargs
    if hasattr(app, 'post_prepare_callback'):
        getattr(app, 'post_prepare_callback')(global_conf, **kwargs)


def thread_pool_server_runner(app, global_conf, **kwargs):
    host = kwargs.get('host', '0.0.0.0')
    port = int(kwargs.get('port', 9090))
    pool_size = int(kwargs.get('pool_size', 10))
    transport = TSocket.TServerSocket(host=host, port=port)
    #transport.host = host
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TThreadPoolServer(app, transport, tfactory, pfactory)
    if pool_size:
        server.threads = pool_size

    server.prepare()

    post_prepare(app, global_conf, **kwargs)

    server.serve()


def nonblock_server_runner(app, global_conf, **kwargs):
    host = kwargs.get('host', '0.0.0.0')
    port = int(kwargs.get('port', 9090))
    transport = TSocket.TServerSocket(host=host, port=port)
    #transport.host = host
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TNonblockingServer(app, transport, pfactory, pfactory)

    server.prepare()

    post_prepare(app, global_conf, **kwargs)

    server.serve()
