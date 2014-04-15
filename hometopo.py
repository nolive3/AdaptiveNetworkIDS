from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from mininet.node import Controller
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
_controller = Controller('Internet Controller', port=6666)
_remControl = RemoteController('Remote Controller')
_controllers = {'local': _controller, 'remote': _remControl}
_translation = {'s0': 'local', 's1': 'local', 's2': 'remote', 's3': 'remote'}

class MultiController(OVSSwitch):
    def start(self, controllers):
        print(self.name)
        return OVSSwitch.start(self, [_controllers[_translation[self.name]]])

# A typical home network
class HomeTopo(Topo):
    "Mininet test topology"
    
    def __init__(self, ethHosts = 1, wifiHosts = 0, hostConfig = {'cpu': 0.1}, internetLinkConfig = {'bw': 10, 'delay': '10ms', 'loss': 0, 'max_queue_size': None }, wifiLinkConfig = {'bw': 1, 'delay': '5ms', 'loss': 10, 'max_queue_size': None }, ethernetLinkConfig = {'bw': 100, 'delay': '1ms', 'loss': 0, 'max_queue_size': None }, **params):
        Topo.__init__(self, **params)
        self.internet = self.addSwitch('s0')
        self.router = self.addSwitch('s1')
        self.switch = self.addSwitch('s2')
        self.wifi = self.addSwitch('s3')

        self.addLink(self.router, self.switch, **ethernetLinkConfig)
        self.addLink(self.wifi, self.switch, **ethernetLinkConfig)
        self.addLink(self.router, self.internet, **internetLinkConfig)

        self.ethHosts = []
        self.wifiHosts = []


        self.remote = self.addHost('remote', **hostConfig)
        self.evil = self.addHost('evil', **hostConfig)

        for i in range(ethHosts):
            self.ethHosts.append(self.addHost('lan'+str(i), **hostConfig))
        for i in range(wifiHosts):
            self.wifiHosts.append(self.addHost('wlan'+str(i), **hostConfig))

        self.addLink(self.remote, self.internet, **internetLinkConfig)
        self.addLink(self.evil, self.internet, **internetLinkConfig)

        for host in self.ethHosts:
            self.addLink(self.switch, host, **ethernetLinkConfig)
        for host in self.wifiHosts:
            self.addLink(self.wifi, host, **wifiLinkConfig)




def main():
    topo = HomeTopo()
    net = Mininet(topo=topo, switch=MultiController, host=CPULimitedHost, 
                  link=TCLink, autoPinCpus=True, build=False)
    net.addController(_controller)
    net.build()
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    main()
