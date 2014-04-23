from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from mininet.node import Controller
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.link import Intf
_controller = Controller('Internet Controller', port=6666)
_remControl = RemoteController('Remote Controller')
_controllers = {'local': _controller, 'remote': _remControl}
_translation = {'s1': 'local', 's2': 'remote', 's3': 'remote'}

class MultiController(OVSSwitch):
    def start(self, controllers):
        print(self.name)
        return OVSSwitch.start(self, [_controllers[_translation[self.name]]])

# A typical home network
class HomeTopo(Topo):
    "Mininet test topology"
    def routerSetup(self, net):
        r = self.internet
        router = net[r]
        hosts = map(lambda x:net[x], self.ethHosts+self.wifiHosts)
        i1 = self.remote
        remote = net[i1]
        i2 = self.evil
        evil = net[i2]
        reth0 = router.IP(intf=r+'-eth0')

        router.setIP(intf=r+'-eth1', ip='192.168.1.1/24')
        remote.setIP(ip='192.168.1.2/24')
        remote.setDefaultRoute('via 192.168.1.1')

        router.setIP(intf=r+'-eth2', ip='192.168.2.1/24')
        evil.setIP(ip='192.168.2.2/24')
        evil.setDefaultRoute('via 192.168.2.1')
 
        self.controller = Intf('eth2', node=net[self.switch])
        #controller.setIP(ip='10.0.0.240/8')
        #controller.setMAC(mac='11:11:11:11:11:11')
        #controller.setDefaultRoute('via %s'%reth0)

        for host in hosts:
            host.setDefaultRoute('via %s'%reth0)

        router.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')


    def __init__(self, ethHosts = 1, wifiHosts = 0, hostConfig = {'cpu': 0.1}, internetLinkConfig = {'bw': 10, 'delay': '10ms', 'loss': 0, 'max_queue_size': None }, wifiLinkConfig = {'bw': 1, 'delay': '5ms', 'loss': 10, 'max_queue_size': None }, ethernetLinkConfig = {'bw': 100, 'delay': '1ms', 'loss': 0, 'max_queue_size': None }, **params):
        Topo.__init__(self, **params)
        self.internet = self.addHost('Internet', **hostConfig)
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

        self.addLink(self.remote, self.internet, **internetLinkConfig)
        self.addLink(self.evil, self.internet, **internetLinkConfig)
        #self.addLink(self.controller, self.switch, **ethernetLinkConfig)

        for i in range(ethHosts):
            self.ethHosts.append(self.addHost('lan'+str(i), **hostConfig))
        for i in range(wifiHosts):
            self.wifiHosts.append(self.addHost('wlan'+str(i), **hostConfig))
        for host in self.ethHosts:
            self.addLink(self.switch, host, **ethernetLinkConfig)
        for host in self.wifiHosts:
            self.addLink(self.wifi, host, **wifiLinkConfig)




def main():
    topo = HomeTopo(ethHosts=4)
    net = Mininet(topo=topo, switch=MultiController, host=CPULimitedHost, 
                  link=TCLink, autoPinCpus=True, build=False)
    net.addController(_controller)
    net.build()
    topo.routerSetup(net)
    net.start()
    dumpNodeConnections(net.hosts)
    CLI( net )
    net.stop()

if __name__ == '__main__':
    main()
