import packets.apis.apimongo as db
from packets.configuration.mongo import MONGO_DB, MONGO_COLLECTION

def _get_packet_list(mac, protocol, env, inidate, enddate):
    packets = db.get_mac_protocol_packets(MONGO_DB, MONGO_COLLECTION, env, mac, protocol, inidate, enddate)
    return db.mongo_cursor_to_list(packets)

def _get_info_arp(packets):
    protocol_info = {}
    # eth src_oui_resolved
    # arp isprobe
    # arp src_proto_ipv4
    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)
    fields = ["src_proto_ipv4"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "arp", fields)
    return protocol_info

def _get_info_basicxid(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    return protocol_info

def _get_info_bjnp(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    return protocol_info

def _get_info_browser(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["windows_version"]
    protocol_info["windows_version"] = db.get_protocol_layer_field_unique(packets, "browser", fields)

    fields = ["server_type"]
    protocol_info["device_type"] = db.get_protocol_layer_field_unique(packets, "browser", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["source_name"]
    protocol_info["hostname"] = db.get_protocol_layer_field_unique(packets, "nbdgm", fields)

    fields = ["destination_name"]
    protocol_info["workgroup"] = db.get_protocol_layer_field_unique(packets, "nbdgm", fields)

    fields = ["comment"]
    protocol_info["extra"] = db.get_protocol_layer_field_unique(packets, "browser", fields)


    return protocol_info

def _get_info_db_lsp_disc(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["srcport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    return protocol_info

def _get_info_dhcp(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["srcport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["option_hostname"]
    protocol_info["hostname"] = db.get_protocol_layer_field_unique(packets, "dhcp", fields)

    fields = ["option_vendor_class_id"]
    protocol_info["vendor_class"] = db.get_protocol_layer_field_unique(packets, "dhcp", fields)

    return protocol_info

def _get_info_dhcpv6(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["srcport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["client_fqdn"]
    protocol_info["hostname"] = db.get_protocol_layer_field_unique(packets, "dhcpv6", fields)

    fields = ["vendorclass_data"]
    protocol_info["vendor_class"] = db.get_protocol_layer_field_unique(packets, "dhcpv6", fields)

    return protocol_info

def _get_info_icmpv6(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ipv6", fields)


    return protocol_info

def _get_info_igmp(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    # TTL sempre vale 1

    return protocol_info

def _get_info_lldp(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)


    return protocol_info


def _get_info_llmnr(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ipv6", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["dns_qry_name"]
    protocol_info["queries"] = db.get_protocol_layer_field_unique(packets, "llmnr", fields)

    return protocol_info

def _get_info_mdns(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["src"]
    protocol_info["ipv6"] = db.get_protocol_layer_field_unique(packets, "ipv6", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["dns_qry_name"]
    protocol_info["queries"] = db.get_protocol_layer_field_unique(packets, "mdns", fields)

    fields = ["dns_resp_name"]
    protocol_info["responses"] = db.get_protocol_layer_field_unique(packets, "mdns", fields)

    fields = ["dns_srv_target"]
    protocol_info["srv_target"] = db.get_protocol_layer_field_unique(packets, "mdns", fields)

    fields = ["dns_srv_port"]
    protocol_info["srv_port"] = db.get_protocol_layer_field_unique(packets, "mdns", fields)

    fields = ["dns_ptr_domain_name"]
    protocol_info["domain"] = db.get_protocol_layer_field_unique(packets, "mdns", fields)

    return protocol_info

def _get_info_nbns(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["name"]
    protocol_info["queries"] = db.get_protocol_layer_field_unique(packets, "nbns", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    return protocol_info

def _get_info_ssdp(packets):
    protocol_info = {}

    fields = ["src_oui_resolved"]
    protocol_info["manufacturer"] = db.get_protocol_layer_field_unique(packets, "eth", fields)

    fields = ["src"]
    protocol_info["ip"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["ttl"]
    protocol_info["ttl"] = db.get_protocol_layer_field_unique(packets, "ip", fields)

    fields = ["dstport"]
    protocol_info["port"] = db.get_protocol_layer_field_unique(packets, "udp", fields)

    fields = ["http_user_agent"]
    protocol_info["user_agent"] = db.get_protocol_layer_field_unique(packets, "ssdp", fields)

    return protocol_info

# Input: mac, protocolo e entorno
# Input: mac, protocolo e entorno
def get_protocol_info(mac, protocol, env, inidate, enddate):
    protocol_info = {}
    if (protocol == "ARP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_arp(packets)
    if (protocol == "BASICXID"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_basicxid(packets)
    if (protocol == "BJNP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_bjnp(packets)
    if (protocol == "BROWSER"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_browser(packets)
    if (protocol == "DB-LSP-DISC"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_db_lsp_disc(packets)
    if (protocol == "DHCP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_dhcp(packets)
    if (protocol == "DHCPV6"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_dhcpv6(packets)
    if (protocol == "ICMPV6"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_icmpv6(packets)
    if (protocol == "IGMP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_igmp(packets)
    if (protocol == "LLDP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_lldp(packets)
    if (protocol == "LLMNR"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_llmnr(packets)
    if (protocol == "MDNS"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_mdns(packets)
    if (protocol == "NBNS"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_nbns(packets)
    if (protocol == "SSDP"):
        packets = _get_packet_list(mac, protocol, env, inidate, enddate)
        protocol_info = _get_info_ssdp(packets)
    return protocol_info
