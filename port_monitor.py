from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import datetime
import os

LOG_FILE = "port_status.log"

class PortMonitor(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PortMonitor, self).__init__(*args, **kwargs)
        self.port_status = {}  # {(dpid, port_no): status}
        self.log_file = open(LOG_FILE, "a")
        self.mac_to_port = {}

    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"
        print(line)
        self.log_file.write(line + "\n")
        self.log_file.flush()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # Install table-miss flow entry (send unknown packets to controller)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=0,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
        self.log(f"Switch connected: DPID={datapath.id}")

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofproto = dp.ofproto
        reason = msg.reason
        port = msg.desc
        port_no = port.port_no
        port_name = port.name.decode('utf-8')

        reason_map = {
            ofproto.OFPPR_ADD: "ADDED",
            ofproto.OFPPR_DELETE: "DELETED",
            ofproto.OFPPR_MODIFY: "MODIFIED",
        }
        reason_str = reason_map.get(reason, "UNKNOWN")

        # Determine link state
        link_down = bool(port.state & ofproto.OFPPS_LINK_DOWN)
        status = "DOWN" if link_down else "UP"

        self.port_status[(dp.id, port_no)] = status

        alert = "⚠️  ALERT" if status == "DOWN" else "✅  INFO"
        self.log(f"{alert} | Switch {dp.id} | Port {port_no} ({port_name}) | "
                 f"Reason: {reason_str} | State: {status}")
        self.display_status()
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Analyze the packet headers
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # Learn the source MAC address to avoid future Packet-Ins
        self.mac_to_port[dpid][src] = in_port

        # Determine the output port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # If the destination is known, install a flow rule to the switch
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            self.add_flow(datapath, 1, match, actions)

        # Send the current packet out
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                   in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
    
    
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                            match=match, instructions=inst)
        datapath.send_msg(mod)

    def display_status(self):
        print("\n--- Current Port Status ---")
        for (dpid, port_no), status in self.port_status.items():
            print(f"  Switch {dpid} | Port {port_no} : {status}")
        print("---------------------------\n")
