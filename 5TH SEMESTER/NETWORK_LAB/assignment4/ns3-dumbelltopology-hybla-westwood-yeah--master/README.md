# ns3-Dumbbell topology-(hybla-westwood-yeah)

Analyze and compare TCP Hybla, TCP Westwood+, and TCP YeAH-TCP performance. Select a Dumbbell
topology with two routers R1 and R2 connected by a (10 Mbps, 50 ms) wired link. Each of the routers is
connected to 3 hosts i.e., H1 to H3 (i.e. senders) are connected to R1 and H4 to H6 (i.e. receivers) are connected
to R2. The hosts are attached with (100 Mbps, 20ms) links. Both the routers use drop-tail queues with queue size
set according to bandwidth-delay product. Senders (i.e. H1, H2 and H3) are attached with TCP Hybla, TCP
Westwood+, and TCP YeAH-TCP agents, respectively. Choose a packet size of 1.3KB and perform the following
task. Make appropriate assumptions wherever necessary.

1. Start only one flow and analyze the throughput over sufficiently long duration. Mention how you select
the duration. Plot of evolution of congestion window w.r.t. time. Perform this experiment with all the
flows attached to all the three sending agents.
2. In next experiment, start 2 other flows sharing the bottleneck while the first one is in progress and
measure the throughput (in Kbps) of each flow. Plot the throughput and evolution of the TCP congestion
window for each of the flow at a steady-state. Report is the maximum throughput observed for each of the
flows?
3. Measure the congestion loss and Goodput over the duration of the experiment for each of the flows.
