#include "headers.h"



typedef uint32_t uint;

using namespace ns3;
using namespace std;

#define ERROR 0.00001

NS_LOG_COMPONENT_DEFINE ("MyApp");

class MyApp: public Application {
	private:
		virtual void StartApplication(void);
		virtual void StopApplication(void);

		void ScheduleTx(void);
		void SendPacket(void);

		Ptr<Socket>     m_Socket;
		Address         m_Peer;
		uint32_t        m_PacketSize;
		uint32_t        m_NPackets;
		DataRate        m_DataRate;
		EventId         m_SendEvent;
		bool            m_Running;
		uint32_t        m_PacketsSent;

	public:
		MyApp();
		virtual ~MyApp();

		void Setup(Ptr<Socket> socket, Address address, uint packetSize, uint nPackets, DataRate dataRate);
		void recv(int numBytesRcvd);

};

MyApp::MyApp(): m_Socket(0),
		    m_Peer(),
		    m_PacketSize(0),
		    m_NPackets(0),
		    m_DataRate(0),
		    m_SendEvent(),
		    m_Running(false),
		    m_PacketsSent(0) {
}

MyApp::~MyApp() {
	m_Socket = 0;
}

void MyApp::Setup(Ptr<Socket> socket, Address address, uint packetSize, uint nPackets, DataRate dataRate) {
	m_Socket = socket;
	m_Peer = address;
	m_PacketSize = packetSize;
	m_NPackets = nPackets;
	m_DataRate = dataRate;
}

void MyApp::StartApplication() {
	m_Running = true;
	m_PacketsSent = 0;
	m_Socket->Bind();
	m_Socket->Connect(m_Peer);
	SendPacket();
}

void MyApp::StopApplication() {
	m_Running = false;
	if(m_SendEvent.IsRunning()) {
		Simulator::Cancel(m_SendEvent);
	}
	if(m_Socket) {
		m_Socket->Close();
	}
}

void MyApp::SendPacket() {
	Ptr<Packet> packet = Create<Packet>(m_PacketSize);
	m_Socket->Send(packet);

	if(++m_PacketsSent < m_NPackets) {
		ScheduleTx();
	}
}

void MyApp::ScheduleTx() {
	if (m_Running) {
		Time tNext(Seconds(m_PacketSize*8/static_cast<double>(m_DataRate.GetBitRate())));
		m_SendEvent = Simulator::Schedule(tNext, &MyApp::SendPacket, this);

	}
}

////////////////////////////////////////////////////////////////////////////
std::map<uint, uint> packetsDropped;
std::map<Address, double> TotalBytesAtSink;
std::map<std::string, double> mapBytesReceivedIPV4, Throughput;

static void packetDrop(FILE* stream, double startTime, uint myId) {
	if(packetsDropped.find(myId) == packetsDropped.end()) {
		packetsDropped[myId] = 0;
	}
	packetsDropped[myId]++;
}

static void CongestionWindowUpdater(FILE *stream, double startTime, uint oldCwnd, uint newCwnd) {
    fprintf(stream, "%s  %s\n",(std::to_string(  Simulator::Now ().GetSeconds () - startTime)).c_str()   , (std::to_string(newCwnd )).c_str() );

	// *stream->GetStream() << Simulator::Now ().GetSeconds () - startTime << "\t" << newCwnd << std::endl;
}

void ThroughtPutData(FILE *stream, double startTime, std::string context, Ptr<const Packet> p, Ptr<Ipv4> ipv4, uint interface) {
	double timeNow = Simulator::Now().GetSeconds();

    if(Throughput.find(context) == Throughput.end())
		Throughput[context] = 0;
	if(mapBytesReceivedIPV4.find(context) == mapBytesReceivedIPV4.end())
		mapBytesReceivedIPV4[context] = 0;

	mapBytesReceivedIPV4[context] += p->GetSize();
	double curSpeed = (((mapBytesReceivedIPV4[context] * 8.0) / 1024)/(timeNow-startTime));
    fprintf(stream, "%s  %s\n",(std::to_string( timeNow-startTime).c_str())  , (std::to_string(curSpeed )).c_str() );

    if(Throughput[context] < curSpeed)
			Throughput[context] = curSpeed;
}


void GoodPutData(FILE *stream, double startTime, std::string context, Ptr<const Packet> p, const Address& addr){
	double timeNow = Simulator::Now().GetSeconds();

	if(TotalBytesAtSink.find(addr) == TotalBytesAtSink.end())
		TotalBytesAtSink[addr] = 0;
	TotalBytesAtSink[addr] += p->GetSize();
	//getting goodput by calculating the average data transfer rate
    double speed = (((TotalBytesAtSink[addr] * 8.0) / 1024)/(timeNow-startTime));
    fprintf(stream, "%s  %s\n",(std::to_string( timeNow-startTime).c_str() ) , (std::to_string(speed )).c_str() );

    

}

Ptr<Socket> WestwoodFlow(Address sinkAddress, 
					uint sinkPort, 
					Ptr<Node> hostNode, 
					Ptr<Node> sinkNode, 
					double startTime, 
					double stopTime,
					uint packetSize,
					uint totalPackets,
					string dataRate,
					double appStartTime,
					double appStopTime) {


    Config::SetDefault ("ns3::TcpWestwood::ProtocolType", EnumValue (TcpWestwood::WESTWOODPLUS));
    Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpWestwood::GetTypeId()));
	
	PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
	ApplicationContainer sinkApps = packetSinkHelper.Install(sinkNode);
	sinkApps.Start(Seconds(startTime));
	sinkApps.Stop(Seconds(stopTime));

	Ptr<Socket> TcpSocket = Socket::CreateSocket(hostNode, TcpSocketFactory::GetTypeId());

    //Run the app to get the data
	Ptr<MyApp> app = CreateObject<MyApp>();
	app->Setup(TcpSocket, sinkAddress, packetSize, totalPackets, DataRate(dataRate));
	hostNode->AddApplication(app);
	app->SetStartTime(Seconds(appStartTime));
	app->SetStopTime(Seconds(appStopTime));

	return TcpSocket;
}

Ptr<Socket> YeahFlow(Address sinkAddress, 
					uint sinkPort, 
					Ptr<Node> hostNode, 
					Ptr<Node> sinkNode, 
					double startTime, 
					double stopTime,
					uint packetSize,
					uint totalPackets,
					string dataRate,
					double appStartTime,
					double appStopTime) {

    Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpYeah::GetTypeId()));
	
	PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
	ApplicationContainer sinkApps = packetSinkHelper.Install(sinkNode);
	sinkApps.Start(Seconds(startTime));
	sinkApps.Stop(Seconds(stopTime));

	Ptr<Socket> TcpSocket = Socket::CreateSocket(hostNode, TcpSocketFactory::GetTypeId());

    //Run the app to get the data
	Ptr<MyApp> app = CreateObject<MyApp>();
	app->Setup(TcpSocket, sinkAddress, packetSize, totalPackets, DataRate(dataRate));
	hostNode->AddApplication(app);
	app->SetStartTime(Seconds(appStartTime));
	app->SetStopTime(Seconds(appStopTime));

	return TcpSocket;
}


Ptr<Socket> HyblaFlow(Address sinkAddress, 
					uint sinkPort, 
					Ptr<Node> hostNode, 
					Ptr<Node> sinkNode, 
					double startTime, 
					double stopTime,
					uint packetSize,
					uint totalPackets,
					string dataRate,
					double appStartTime,
					double appStopTime) {


    Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpYeah::GetTypeId()));
	
	PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
	ApplicationContainer sinkApps = packetSinkHelper.Install(sinkNode);
	sinkApps.Start(Seconds(startTime));
	sinkApps.Stop(Seconds(stopTime));

	Ptr<Socket> TcpSocket = Socket::CreateSocket(hostNode, TcpSocketFactory::GetTypeId());

    //Run the app to get the data
	Ptr<MyApp> app = CreateObject<MyApp>();
	app->Setup(TcpSocket, sinkAddress, packetSize, totalPackets, DataRate(dataRate));
	hostNode->AddApplication(app);
	app->SetStartTime(Seconds(appStartTime));
	app->SetStopTime(Seconds(appStopTime));

	return TcpSocket;
}



int main(){

    uint totalPackets = 1000000;
	uint packetSize = 1.3*1024;		
	uint queueSizeHR = (100000*20)/packetSize;
	uint queueSizeRR = (100*50)/packetSize;
	double runningTime = 100;
	double startTime = 0;
	uint port = 9000;

	string rateHR = "100Mbps";
	string latencyHR = "20ms";
	string rateRR = "10Mbps";
	string latencyRR = "50ms";
	string transferSpeed = "50Mbps";

	double errorP = ERROR;
    Ptr<RateErrorModel> em = CreateObjectWithAttributes<RateErrorModel> ("ErrorRate", DoubleValue (errorP));

	//Mode: Whether to use Bytes (see MaxBytes) or Packets (see MaxPackets) as the maximum queue size metric. 



	PointToPointHelper p2pHTR, p2pRTR;

	p2pRTR.SetDeviceAttribute("DataRate", StringValue(rateRR));
	p2pRTR.SetChannelAttribute("Delay", StringValue(latencyRR));
	p2pRTR.SetQueue("ns3::DropTailQueue", "MaxPackets", UintegerValue(queueSizeRR));

    p2pHTR.SetDeviceAttribute("DataRate", StringValue(rateHR));
	p2pHTR.SetChannelAttribute("Delay", StringValue(latencyHR));
	p2pHTR.SetQueue("ns3::DropTailQueue", "MaxPackets", UintegerValue(queueSizeHR));

    NodeContainer nodes;
    nodes.Create(8);

    NodeContainer h1r1 = NodeContainer (nodes.Get (0), nodes.Get (3)); //h1r1
    NodeContainer h2r1 = NodeContainer (nodes.Get (1), nodes.Get (3));
    NodeContainer h3r1 = NodeContainer (nodes.Get (2), nodes.Get (3));
    NodeContainer h4r2 = NodeContainer (nodes.Get (5), nodes.Get (4));
    NodeContainer h5r2 = NodeContainer (nodes.Get (6), nodes.Get (4));
    NodeContainer h6r2 = NodeContainer (nodes.Get (7), nodes.Get (4));
    NodeContainer r1r2 = NodeContainer (nodes.Get (3), nodes.Get (4));

    InternetStackHelper internet;
    internet.Install (nodes);    
    
    cout << "Installing p2p links in the dubmbell" << endl;
    NetDeviceContainer n_h1r1 = p2pHTR.Install (h1r1);
    NetDeviceContainer n_h2r1 = p2pHTR.Install (h2r1);
    NetDeviceContainer n_h3r1 = p2pHTR.Install (h3r1);
    NetDeviceContainer n_h4r2 = p2pHTR.Install (h4r2);
    NetDeviceContainer n_h5r2 = p2pHTR.Install (h5r2);
    NetDeviceContainer n_h6r2 = p2pHTR.Install (h6r2);
    NetDeviceContainer n_r1r2 = p2pHTR.Install (r1r2);

    n_h1r1.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    n_h2r1.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    n_h3r1.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    n_h4r2.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    n_h5r2.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    n_h6r2.Get(1)->SetAttribute("ReceiveErrorModel", PointerValue(em));

    


    std::cout << "Adding IP addresses" << std::endl;
    Ipv4AddressHelper ipv4;
    ipv4.SetBase ("100.101.1.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h1r1 = ipv4.Assign (n_h1r1);

    ipv4.SetBase ("100.101.2.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h2r1 = ipv4.Assign (n_h2r1);

    ipv4.SetBase ("100.101.3.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h3r1 = ipv4.Assign (n_h3r1);

    ipv4.SetBase ("100.101.5.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h4r2 = ipv4.Assign (n_h4r2);

    ipv4.SetBase ("100.101.6.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h5r2 = ipv4.Assign (n_h5r2);

    ipv4.SetBase ("100.101.7.0", "255.255.255.0");
    Ipv4InterfaceContainer i_h6r2 = ipv4.Assign (n_h6r2);

    ipv4.SetBase ("100.101.4.0", "255.255.255.0");
    Ipv4InterfaceContainer i_r1r2 = ipv4.Assign (n_r1r2);


    //////////////////////////////////////////////////////////////////////////////

	

    AsciiTraceHelper asciiTraceHelper;

    FILE * streamPacketDropData1,*streamCongestionWindowData1,*streamThroughputData1,*streamGoodPutData1;
    streamPacketDropData1 = fopen ("B_Yeah_app3_h1_h4_congestion_loss.txt","w");
    streamCongestionWindowData1 = fopen ("B_Yeah_app3_h1_h4_cwnd.txt","w");
    streamThroughputData1 = fopen ("B_Yeah_app3_h1_h4_tp.txt","w");
    streamGoodPutData1 = fopen ("B_Yeah_app3_h1_h4_gp.txt","w"); 

    //tcpYeah stimulation
	Ptr<Socket> TcpYeahSocket = YeahFlow(InetSocketAddress( i_h4r2.GetAddress(0), port), port, nodes.Get(0), nodes.Get(5), startTime, startTime+runningTime, packetSize, totalPackets, transferSpeed, startTime, startTime+runningTime);
	
	// Measure PacketSinks
	string sinkYeah1 = "/NodeList/5/ApplicationList/0/$ns3::PacketSink/Rx";
	Config::Connect(sinkYeah1, MakeBoundCallback(&GoodPutData, streamGoodPutData1, startTime));

	string sinkYeah2 = "/NodeList/5/$ns3::Ipv4L3Protocol/Rx";
	Config::Connect(sinkYeah2, MakeBoundCallback(&ThroughtPutData, streamThroughputData1, startTime));

    TcpYeahSocket->TraceConnectWithoutContext("Drop", MakeBoundCallback (&packetDrop, streamPacketDropData1, startTime, 1));
    TcpYeahSocket->TraceConnectWithoutContext("CongestionWindow", MakeBoundCallback (&CongestionWindowUpdater, streamCongestionWindowData1, startTime));


    // //increment start TIme
	startTime += runningTime;


    FILE * streamPacketDropData2,*streamCongestionWindowData2,*streamThroughputData2,*streamGoodPutData2;
    streamPacketDropData2 = fopen ("B_Hybla_app3_h2_h5_congestion_loss.txt","w");
    streamCongestionWindowData2 = fopen ("B_Hybla_app3_h2_h5_cwnd.txt","w");
    streamThroughputData2 = fopen ("B_Hybla_app3_h2_h5_tp.txt","w");
    streamGoodPutData2 = fopen ("B_Hybla_app3_h2_h5_gp.txt","w"); 
    // //tcpHybla Simulation

	Ptr<Socket> TcpHyblaSocket = HyblaFlow(InetSocketAddress(i_h5r2.GetAddress(0), port), port, nodes.Get(1), nodes.Get(6), startTime+30, startTime+runningTime+30, packetSize, totalPackets, transferSpeed, startTime, startTime+runningTime);


	// Measure PacketSinks
	string sinkHybla1 = "/NodeList/6/ApplicationList/0/$ns3::PacketSink/Rx";
	Config::Connect(sinkHybla1, MakeBoundCallback(&GoodPutData, streamGoodPutData2, startTime));

	string sinkHybla2 = "/NodeList/6/$ns3::Ipv4L3Protocol/Rx";
	Config::Connect(sinkHybla2, MakeBoundCallback(&ThroughtPutData, streamThroughputData2, startTime));

	TcpHyblaSocket->TraceConnectWithoutContext("Drop", MakeBoundCallback (&packetDrop, streamPacketDropData2, startTime, 2));
    TcpHyblaSocket->TraceConnectWithoutContext("CongestionWindow", MakeBoundCallback (&CongestionWindowUpdater, streamCongestionWindowData2, startTime));

    //increment start TIme
	startTime += runningTime;



    // //westWood Plus Stimulation

    FILE * streamPacketDropData3,*streamCongestionWindowData3,*streamThroughputData3,*streamGoodPutData3;
    streamPacketDropData3 = fopen ("B_Westwood_app3_h3_h6_congestion_loss.txt","w");
    streamCongestionWindowData3 = fopen ("B_Westwood_app3_h3_h6_cwnd.txt","w");
    streamThroughputData3 = fopen ("B_Westwood_app3_h3_h6_tp.txt","w");
    streamGoodPutData3 = fopen ("B_Westwood_app3_h3_h6_gp.txt","w"); 

	Ptr<Socket> westwoodPSocket = WestwoodFlow(InetSocketAddress(i_h6r2.GetAddress(0), port), port, nodes.Get(2), nodes.Get(7), startTime+30, startTime+runningTime+30, packetSize, totalPackets, transferSpeed, startTime, startTime+runningTime);

	// Measure PacketSinks
	string sinkWestwood1 = "/NodeList/7/ApplicationList/0/$ns3::PacketSink/Rx";
	Config::Connect(sinkWestwood1, MakeBoundCallback(&GoodPutData, streamGoodPutData3, startTime));

	string sinkWestwood2 = "/NodeList/7/$ns3::Ipv4L3Protocol/Rx";
	Config::Connect(sinkWestwood2, MakeBoundCallback(&ThroughtPutData, streamThroughputData3, startTime));

    westwoodPSocket->TraceConnectWithoutContext("Drop", MakeBoundCallback (&packetDrop, streamPacketDropData3, startTime, 3));
    westwoodPSocket->TraceConnectWithoutContext("CongestionWindow", MakeBoundCallback (&CongestionWindowUpdater, streamCongestionWindowData3, startTime));

    //increment start TIme
	 startTime += runningTime;



    ////////running the flow monitor for anylyzing the code
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();


	Ptr<FlowMonitor> flowmon;
	FlowMonitorHelper flowmonHelper;
	flowmon = flowmonHelper.InstallAll();
	Simulator::Stop(Seconds(startTime+runningTime+30));
	Simulator::Run();
	flowmon->CheckForLostPackets();

	//Ptr<OutputStreamWrapper> streamTP = asciiTraceHelper.CreateFileStream("application_6_a.tp");
	Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmonHelper.GetClassifier());
	std::map<FlowId, FlowMonitor::FlowStats> stats = flowmon->GetFlowStats();

	for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i) {
		Ipv4FlowClassifier::FiveTuple tempClassifier = classifier->FindFlow (i->first);

        if (tempClassifier.sourceAddress=="100.101.1.1"){

		    // *streamPacketDropData1->GetStream() << "Tcp Yeah Flow " << i->first  << " (" << (tempClassifier.sourceAddress) << " -> " << tempClassifier.destinationAddress << ")\n";
		    fprintf(streamPacketDropData1, "TCP Yeah flow %s (100.101.1.1 -> 100.101.5.1)\n",(std::to_string( i->first)).c_str());
            fprintf(streamPacketDropData1, "Total Packet Lost:%s\n",(std::to_string( i->second.lostPackets)).c_str() );
            fprintf(streamPacketDropData1, "Packet Lost due to buffer overflow:%s\n",(std::to_string( packetsDropped[1] )).c_str() );
            fprintf(streamPacketDropData1, "Packet Lost due to Congestion:%s\n",(std::to_string( i->second.lostPackets - packetsDropped[1] )).c_str() );
            fprintf(streamPacketDropData1, "Maximum throughput(in kbps):%s\n",(std::to_string( Throughput["/NodeList/5/$ns3::Ipv4L3Protocol/Rx"] )).c_str() );
            fprintf(streamPacketDropData1, "Total Packets transmitted:%s\n",(std::to_string( totalPackets )).c_str() );
            fprintf(streamPacketDropData1, "Packets Successfully Transferred:%s\n",(std::to_string(  totalPackets- i->second.lostPackets )).c_str() );
            fprintf(streamPacketDropData1, "Percentage of packet loss (total):%s\n",(std::to_string( double(i->second.lostPackets*100)/double(totalPackets) )).c_str() );
		    fprintf(streamPacketDropData1, "Percentage of packet loss (due to buffer overflow):%s\n",(std::to_string(  double(packetsDropped[1]*100)/double(totalPackets))).c_str() );
		    fprintf(streamPacketDropData1, "Percentage of packet loss (duee to congestion):%s\n",(std::to_string( double((i->second.lostPackets - packetsDropped[1])*100)/double(totalPackets))).c_str() );

 
	
		}
        else if(tempClassifier.sourceAddress=="100.101.2.1"){
            fprintf(streamPacketDropData2, "TCP Hybla flow %s (100.101.2.1 -> 100.101.6.1)\n",(std::to_string( i->first)).c_str());
            fprintf(streamPacketDropData2, "Total Packet Lost:%s\n",(std::to_string( i->second.lostPackets)).c_str() );
            fprintf(streamPacketDropData2, "Packet Lost due to buffer overflow:%s\n",(std::to_string( packetsDropped[2] )).c_str() );
            fprintf(streamPacketDropData2, "Packet Lost due to Congestion:%s\n",(std::to_string( i->second.lostPackets - packetsDropped[2] )).c_str() );
            fprintf(streamPacketDropData2, "Maximum throughput(in kbps):%s\n",(std::to_string( Throughput["/NodeList/6/$ns3::Ipv4L3Protocol/Rx"] )).c_str() );
            fprintf(streamPacketDropData2, "Total Packets transmitted:%s\n",(std::to_string( totalPackets )).c_str() );
            fprintf(streamPacketDropData2, "Packets Successfully Transferred:%s\n",(std::to_string(  totalPackets- i->second.lostPackets )).c_str() );
            fprintf(streamPacketDropData2, "Percentage of packet loss (total):%s\n",(std::to_string( double(i->second.lostPackets*100)/double(totalPackets) )).c_str() );
		    fprintf(streamPacketDropData2, "Percentage of packet loss (due to buffer overflow):%s\n",(std::to_string(  double(packetsDropped[2]*100)/double(totalPackets))).c_str() );
		    fprintf(streamPacketDropData2, "Percentage of packet loss (duee to congestion):%s\n",(std::to_string( double((i->second.lostPackets - packetsDropped[2])*100)/double(totalPackets))).c_str() );
        }
        else if(tempClassifier.sourceAddress=="100.101.3.1"){
            fprintf(streamPacketDropData3, "TCP Westwood+ flow %s (100.101.3.1 -> 100.101.7.1)\n",(std::to_string( i->first)).c_str());
            fprintf(streamPacketDropData3, "Total Packet Lost:%s\n",(std::to_string( i->second.lostPackets)).c_str() );
            fprintf(streamPacketDropData3, "Packet Lost due to buffer overflow:%s\n",(std::to_string( packetsDropped[3] )).c_str() );
            fprintf(streamPacketDropData3, "Packet Lost due to Congestion:%s\n",(std::to_string( i->second.lostPackets - packetsDropped[3] )).c_str() );
            fprintf(streamPacketDropData3, "Maximum throughput(in kbps):%s\n",(std::to_string( Throughput["/NodeList/7/$ns3::Ipv4L3Protocol/Rx"] )).c_str() );
            fprintf(streamPacketDropData3, "Total Packets transmitted:%s\n",(std::to_string( totalPackets )).c_str() );
            fprintf(streamPacketDropData3, "Packets Successfully Transferred:%s\n",(std::to_string(  totalPackets- i->second.lostPackets )).c_str() );
            fprintf(streamPacketDropData3, "Percentage of packet loss (total):%s\n",(std::to_string( double(i->second.lostPackets*100)/double(totalPackets) )).c_str() );
		    fprintf(streamPacketDropData3, "Percentage of packet loss (due to buffer overflow):%s\n",(std::to_string(  double(packetsDropped[3]*100)/double(totalPackets))).c_str() );
		    fprintf(streamPacketDropData3, "Percentage of packet loss (duee to congestion):%s\n",(std::to_string( double((i->second.lostPackets - packetsDropped[3])*100)/double(totalPackets))).c_str() );
        }

	}

	//flowmon->SerializeToXmlFile("application_6_a.flowmon", true, true);
	std::cout << "Simulation finished" << std::endl;
	Simulator::Destroy();

    return 0;
}