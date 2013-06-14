from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server.TServer import TThreadPoolServer
from thrift.server.TNonblockingServer import TNonblockingServer


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
