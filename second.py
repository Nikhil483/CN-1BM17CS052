
import ns.core
import ns.network
import ns.csma
import ns.internet
import ns.point_to_point
import ns.applications
import sys

# // Default Network Topology
# //
# //       10.1.1.0
# // n0 -------------- n1   n2   n3   n4
# //    point-to-point  |    |    |    |
# //                    ================
# //                      LAN 10.1.2.0

cmd = ns.core.CommandLine()
cmd.nCsma = 2
cmd.verbose = "True"
cmd.AddValue("nCsma", "Number of \"extra\" CSMA nodes/devices")
cmd.AddValue("verbose", "Tell echo applications to log if true")
cmd.Parse(sys.argv)

nCsma = int(cmd.nCsma)
verbose = cmd.verbose

if verbose == "True":
	ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
	ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
nCsma = 1 if int(nCsma) == 0 else int(nCsma)

p2pNodes = ns.network.NodeContainer()
p2pNodes.Create(2)
p2pNodes1 = ns.network.NodeContainer()
p2pNodes1.Create(2)

csmaNodes = ns.network.NodeContainer()
csmaNodes.Add(p2pNodes.Get(1))
csmaNodes.Add(p2pNodes1.Get(0))
csmaNodes.Create(nCsma)

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

p2pDevices = pointToPoint.Install(p2pNodes)


csma = ns.csma.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))

csmaDevices = csma.Install(csmaNodes)

stack = ns.internet.InternetStackHelper()
stack.Install(p2pNodes.Get(0))
stack.Install(p2pNodes1.Get(1))
stack.Install(csmaNodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
p2pInterfaces = address.Assign(p2pDevices)

address1 = ns.internet.Ipv4AddressHelper()
address1.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
p2pInterfaces1 = address1.Assign(p2pDevices)

address.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
csmaInterfaces = address.Assign(csmaDevices)


echoServer = ns.applications.UdpEchoServerHelper(9)
echoServer1 = ns.applications.UdpEchoServerHelper(10)

serverApps = echoServer.Install(csmaNodes.Get(nCsma))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

serverApps1 = echoServer1.Install(csmaNodes.Get(nCsma))
serverApps1.Start(ns.core.Seconds(1.0))
serverApps1.Stop(ns.core.Seconds(10.0))

echoClient = ns.applications.UdpEchoClientHelper(csmaInterfaces.GetAddress(nCsma), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

echoClient1 = ns.applications.UdpEchoClientHelper(csmaInterfaces.GetAddress(nCsma), 10)
echoClient1.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient1.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
echoClient1.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps = echoClient.Install(p2pNodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))
clientApps1 = echoClient1.Install(p2pNodes.Get(1))
clientApps1.Start(ns.core.Seconds(3.0))
clientApps1.Stop(ns.core.Seconds(10.0))

ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

pointToPoint.EnablePcapAll("second")
csma.EnablePcap ("second", csmaDevices.Get (1), True)

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()

