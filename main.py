import os
import sys
import json
import socket
import struct
import random
import threading
import time
from pathlib import Path

os.environ['KIVY_LOG_LEVEL'] = 'warning'

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.divider import MDDivider
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.widget import MDWidget

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

MDBoxLayout:
    orientation: "vertical"
    md_bg_color: get_color_from_hex("#0A0A0F")

    MDBoxLayout:
        size_hint_y: None
        height: dp(56)
        padding: dp(16), 0
        md_bg_color: get_color_from_hex("#12121A")
        elevation: dp(4)

        MDLabel:
            text: "KiwiBypass"
            font_style: "Title"
            role: "large"
            bold: True
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#00E676")
            halign: "left"
            valign: "center"

        MDLabel:
            text: "DPI Shield"
            font_style: "Label"
            role: "small"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#666666")
            halign: "right"
            valign: "center"

    MDScreenManager:
        id: screen_manager

        MDScreen:
            name: "home"

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(16)

                MDCard:
                    size_hint_y: None
                    height: dp(200)
                    radius: dp(20)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(20)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(12)

                        MDLabel:
                            text: "Durum"
                            font_style: "Label"
                            role: "small"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#888888")

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: dp(12)

                            MDBoxLayout:
                                id: status_indicator
                                size_hint_x: None
                                width: dp(12)
                                size_hint_y: None
                                height: dp(12)
                                pos_hint: {"center_y": 0.5}
                                md_bg_color: get_color_from_hex("#FF1744")
                                radius: [dp(6)]

                            MDLabel:
                                id: status_text
                                text: "Beklemede"
                                font_style: "Headline"
                                role: "small"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#FFFFFF")

                        MDLabel:
                            id: status_detail
                            text: "Proxy durakli"
                            font_style: "Label"
                            role: "small"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#666666")

                        MDWidget:
                            size_hint_y: None
                            height: dp(1)

                        MDButton:
                            id: main_button
                            style: "filled"
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.6
                            on_release: app.toggle_proxy()
                            theme_bg_color: "Custom"
                            bg_color: get_color_from_hex("#00E676")

                            MDButtonIcon:
                                icon: "play"

                            MDButtonText:
                                id: main_button_text
                                text: "BASLAT"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#000000")

                MDCard:
                    size_hint_y: None
                    height: dp(180)
                    radius: dp(20)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(20)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)

                        MDLabel:
                            text: "Ayrintilar"
                            font_style: "Label"
                            role: "small"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#888888")

                        MDBoxLayout:
                            orientation: "horizontal"

                            MDLabel:
                                text: "Tip:"
                                font_style: "Label"
                                role: "small"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#666666")

                            MDLabel:
                                id: detail_type
                                text: "DNS + Fragmentation"
                                font_style: "Label"
                                role: "small"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#00E676")

                        MDBoxLayout:
                            orientation: "horizontal"

                            MDLabel:
                                text: "Port:"
                                font_style: "Label"
                                role: "small"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#666666")

                            MDLabel:
                                id: detail_port
                                text: "8888"
                                font_style: "Label"
                                role: "small"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#FFFFFF")

                        MDBoxLayout:
                            orientation: "horizontal"

                            MDLabel:
                                text: "DNS:"
                                font_style: "Label"
                                role: "small"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#666666")

                            MDLabel:
                                id: detail_dns
                                text: "1.1.1.1 (Cloudflare)"
                                font_style: "Label"
                                role: "small"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#FFFFFF")

                        MDBoxLayout:
                            orientation: "horizontal"

                            MDLabel:
                                text: "Engellenen:"
                                font_style: "Label"
                                role: "small"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#666666")

                            MDLabel:
                                id: detail_blocked
                                text: "0 paket"
                                font_style: "Label"
                                role: "small"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#FF9100")

        MDScreen:
            name: "settings"

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)

                MDLabel:
                    text: "Ayarlar"
                    font_style: "Headline"
                    role: "medium"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#FFFFFF")
                    size_hint_y: None
                    height: dp(40)

                MDCard:
                    radius: dp(16)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(16)
                    size_hint_y: None
                    height: dp(300)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(48)

                            MDBoxLayout:
                                orientation: "vertical"

                                MDLabel:
                                    text: "Mod Secin"
                                    font_style: "Title"
                                    role: "small"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#FFFFFF")

                                MDLabel:
                                    text: "DPI bypass yontemi"
                                    font_style: "Label"
                                    role: "small"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#666666")

                            MDButton:
                                id: mod_button
                                style: "outlined"
                                on_release: app.open_mod_menu()
                                size_hint_x: None
                                width: dp(180)

                                MDButtonText:
                                    id: mod_text
                                    text: "DNS + Frag"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#00E676")

                                MDButtonIcon:
                                    icon: "menu-down"

                        MDDivider:
                            color: get_color_from_hex("#2A2A3E")

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(48)

                            MDBoxLayout:
                                orientation: "vertical"

                                MDLabel:
                                    text: "DNS Sunucusu"
                                    font_style: "Title"
                                    role: "small"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#FFFFFF")

                                MDLabel:
                                    text: "Cozumleme sunucusu"
                                    font_style: "Label"
                                    role: "small"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#666666")

                            MDButton:
                                id: dns_button
                                style: "outlined"
                                on_release: app.open_dns_menu()
                                size_hint_x: None
                                width: dp(180)

                                MDButtonText:
                                    id: dns_text
                                    text: "Cloudflare"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#00E676")

                                MDButtonIcon:
                                    icon: "menu-down"

                        MDDivider:
                            color: get_color_from_hex("#2A2A3E")

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(48)

                            MDBoxLayout:
                                orientation: "vertical"

                                MDLabel:
                                    text: "Parcalama Boyutu"
                                    font_style: "Title"
                                    role: "small"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#FFFFFF")

                                MDLabel:
                                    text: "Paket boyutu (byte)"
                                    font_style: "Label"
                                    role: "small"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#666666")

                            MDButton:
                                id: frag_button
                                style: "outlined"
                                on_release: app.open_frag_menu()
                                size_hint_x: None
                                width: dp(180)

                                MDButtonText:
                                    id: frag_text
                                    text: "Kucuk (2-4)"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#00E676")

                                MDButtonIcon:
                                    icon: "menu-down"

                        MDDivider:
                            color: get_color_from_hex("#2A2A3E")

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(48)

                            MDBoxLayout:
                                orientation: "vertical"

                                MDLabel:
                                    text: "Otomatik DNS"
                                    font_style: "Title"
                                    role: "small"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#FFFFFF")

                                MDLabel:
                                    text: "DNS ayarini degistir"
                                    font_style: "Label"
                                    role: "small"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#666666")

                            MDSwitch:
                                id: auto_dns_switch
                                active: True
                                on_active: app.toggle_auto_dns(self.active)

                MDCard:
                    radius: dp(16)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(16)
                    size_hint_y: None
                    height: dp(200)

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)

                        MDLabel:
                            text: "Ozel DNS"
                            font_style: "Title"
                            role: "small"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFFFFF")
                            size_hint_y: None
                            height: dp(24)

                        MDLabel:
                            text: "DNS IP adresi girin"
                            font_style: "Label"
                            role: "small"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#666666")
                            size_hint_y: None
                            height: dp(20)

                        MDTextField:
                            id: custom_dns_field
                            hint_text: "1.1.1.1"
                            mode: "outlined"
                            size_hint_y: None
                            height: dp(48)

                        MDButton:
                            style: "filled"
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.5
                            on_release: app.save_custom_dns()
                            theme_bg_color: "Custom"
                            bg_color: get_color_from_hex("#00E676")

                            MDButtonText:
                                text: "Kaydet"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#000000")

        MDScreen:
            name: "domains"

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(40)

                    MDLabel:
                        text: "Engellenenler"
                        font_style: "Headline"
                        role: "medium"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFFFFF")

                    MDButton:
                        style: "text"
                        on_release: app.reset_domains()
                        size_hint_x: None
                        width: dp(100)

                        MDButtonText:
                            text: "Sifirla"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF9100")

                MDCard:
                    radius: dp(16)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(8)
                    size_hint_y: 0.9

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(4)

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(48)
                            padding: dp(8)

                            MDTextField:
                                id: add_domain_field
                                hint_text: "domain ekle: discord.com"
                                mode: "outlined"
                                size_hint_x: 0.7
                                size_hint_y: None
                                height: dp(40)

                            MDButton:
                                style: "filled"
                                size_hint_x: 0.3
                                on_release: app.add_domain()
                                theme_bg_color: "Custom"
                                bg_color: get_color_from_hex("#00E676")

                                MDButtonIcon:
                                    icon: "plus"

                                MDButtonText:
                                    text: "Ekle"
                                    theme_text_color: "Custom"
                                    text_color: get_color_from_hex("#000000")

                        ScrollView:
                            MDBoxLayout:
                                id: domain_list
                                orientation: "vertical"
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: dp(4)
                                padding: dp(4)

        MDScreen:
            name: "logs"

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(40)

                    MDLabel:
                        text: "Kayitlar"
                        font_style: "Headline"
                        role: "medium"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFFFFF")

                    MDButton:
                        style: "text"
                        on_release: app.clear_logs()
                        size_hint_x: None
                        width: dp(100)

                        MDButtonText:
                            text: "Temizle"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF9100")

                MDCard:
                    radius: dp(16)
                    md_bg_color: get_color_from_hex("#1A1A2E")
                    padding: dp(8)

                    ScrollView:
                        MDLabel:
                            id: log_text
                            text: "Baslatilmadi..."
                            font_style: "Label"
                            role: "small"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#00E676")
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            halign: "left"
                            valign: "top"
                            markup: True

    MDBoxLayout:
        size_hint_y: None
        height: dp(64)
        md_bg_color: get_color_from_hex("#12121A")
        padding: dp(8), dp(4)
        spacing: dp(4)

        MDButton:
            style: "text"
            on_release: app.switch_screen("home")
            pos_hint: {"center_x": 0.5}

            MDButtonIcon:
                icon: "home"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#00E676")

        MDButton:
            style: "text"
            on_release: app.switch_screen("settings")
            pos_hint: {"center_x": 0.5}

            MDButtonIcon:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#888888")

        MDButton:
            style: "text"
            on_release: app.switch_screen("domains")
            pos_hint: {"center_x": 0.5}

            MDButtonIcon:
                icon: "shield-lock"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#888888")

        MDButton:
            style: "text"
            on_release: app.switch_screen("logs")
            pos_hint: {"center_x": 0.5}

            MDButtonIcon:
                icon: "text-box"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#888888")
'''

DEFAULT_DOMAINS = [
    "discord.com", "discord.gg", "discordapp.com",
    "gateway.discord.gg", "cdn.discordapp.com",
    "media.discordapp.net", "status.discord.com",
    "youtube.com", "www.youtube.com",
    "google.com", "googleapis.com",
    "t.me", "telegram.org",
    "twitter.com", "x.com",
    "facebook.com", "instagram.com",
    "whatsapp.com",
    "reddit.com",
    "twitch.tv",
    "spotify.com",
]

DNS_SERVERS = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9",
    "OpenDNS": "208.67.222.222",
    "AdGuard": "94.140.14.14",
}

FRAG_SIZES = {
    "Kucuk (2-4)": (2, 4),
    "Orta (4-8)": (4, 8),
    "Buyuk (8-16)": (8, 16),
    "Rastgele": (2, 16),
}

MODS = {
    "DNS + Frag": "dns_frag",
    "Sadece DNS": "dns_only",
    "Sadece Frag": "frag_only",
    "Tumu": "all",
}


class DnsResolver:
    def __init__(self, dns_server="1.1.1.1"):
        self.dns_server = dns_server

    def build_dns_query(self, domain):
        tx_id = random.randint(0, 65535)
        flags = 0x0100
        questions = 1
        header = struct.pack(">HHHHHH", tx_id, flags, questions, 0, 0, 0)
        query = b""
        for part in domain.encode().split(b"."):
            query += bytes([len(part)]) + part
        query += b"\x00"
        query += struct.pack(">HH", 1, 1)
        return header + query

    def parse_dns_response(self, data):
        try:
            answers = struct.unpack(">H", data[6:8])[0]
            idx = 12
            while idx < len(data):
                length = data[idx]
                if length == 0:
                    idx += 1
                    break
                idx += length + 1
            idx += 4
            ips = []
            for _ in range(answers):
                if idx + 1 > len(data):
                    break
                if data[idx] & 0xC0 == 0xC0:
                    idx += 2
                else:
                    while idx < len(data):
                        length = data[idx]
                        if length == 0:
                            idx += 1
                            break
                        idx += length + 1
                if idx + 10 > len(data):
                    break
                rtype, rclass, ttl = struct.unpack(">HHI", data[idx:idx + 8])
                idx += 8
                rdlength = struct.unpack(">H", data[idx:idx + 2])[0]
                idx += 2
                if rtype == 1 and rdlength == 4 and idx + 4 <= len(data):
                    ips.append(socket.inet_ntoa(data[idx:idx + 4]))
                idx += rdlength
            return ips
        except Exception:
            return []

    def resolve(self, domain):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            query = self.build_dns_query(domain)
            sock.sendto(query, (self.dns_server, 53))
            response, _ = sock.recvfrom(512)
            sock.close()
            return self.parse_dns_response(response)
        except Exception:
            return []


class ProxyEngine:
    def __init__(self):
        self.running = False
        self.server_socket = None
        self.dns_resolver = DnsResolver()
        self.blocked_domains = list(DEFAULT_DOMAINS)
        self.fragment_size_min = 2
        self.fragment_size_max = 4
        self.mode = "dns_frag"
        self.port = 8888
        self.blocked_count = 0
        self.auto_dns = True
        self.log_callback = None

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def is_blocked(self, host):
        host = host.lower().strip()
        for d in self.blocked_domains:
            if host == d or host.endswith("." + d):
                return True
        return False

    def find_sni_offset(self, data):
        if len(data) < 50 or data[0] != 0x16:
            return None
        try:
            i = 5 + 4
            i += 2 + 32
            if i >= len(data):
                return None
            sid_len = data[i]
            i += 1 + sid_len
            if i + 2 > len(data):
                return None
            cs_len = struct.unpack(">H", data[i:i + 2])[0]
            i += 2 + cs_len
            if i >= len(data):
                return None
            cm_len = data[i]
            i += 1 + cm_len
            if i + 2 > len(data):
                return None
            ext_total = struct.unpack(">H", data[i:i + 2])[0]
            i += 2
            ext_end = i + ext_total
            while i + 4 <= ext_end and i + 4 <= len(data):
                etype = struct.unpack(">H", data[i:i + 2])[0]
                elen = struct.unpack(">H", data[i + 2:i + 4])[0]
                edata = i + 4
                if etype == 0 and edata + 5 <= len(data):
                    return edata + 5
                i = edata + elen
        except Exception:
            return None
        return None

    def send_fragmented(self, sock, data):
        try:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass

        sni = self.find_sni_offset(data)
        if sni and sni < len(data) - 1:
            sock.sendall(data[:sni])
            time.sleep(0.015)
            sock.sendall(data[sni:])
        elif len(data) > 1:
            sock.sendall(data[:1])
            time.sleep(0.015)
            sock.sendall(data[1:])
        else:
            sock.sendall(data)
    def handle_connection(self, client_socket, addr):
        try:
            data = client_socket.recv(8192)
            if not data:
                client_socket.close()
                return

            first_line = data.split(b"\r\n")[0].decode("utf-8", errors="ignore")
            method = first_line.split(" ")[0] if " " in first_line else ""

            host = ""
            port = 443
            is_connect = method == "CONNECT"

            if is_connect:
                parts = first_line.split(" ")
                if len(parts) >= 2:
                    host_port = parts[1]
                    host = host_port.split(":")[0]
                    if ":" in host_port:
                        port = int(host_port.split(":")[1])
            else:
                port = 80
                parts = first_line.split(" ")
                if len(parts) >= 2 and parts[1].startswith("http"):
                    target = parts[1]
                    rest = target[7:]
                    if ":" in rest and rest.find("/") > rest.find(":"):
                        try:
                            port = int(rest.split("/")[0].split(":")[1])
                        except Exception:
                            port = 80
                for line in data.split(b"\r\n"):
                    if line.lower().startswith(b"host:"):
                        host_part = line[5:].decode("utf-8", errors="ignore").strip()
                        if ":" in host_part:
                            host = host_part.split(":")[0]
                            port = int(host_part.split(":")[1])
                        else:
                            host = host_part

            if not host:
                client_socket.close()
                return

            target = host
            if self.is_blocked(host):
                self.blocked_count += 1
                self.log(f"[BLOCKED] {host} -> parcalaniyor...")

            try:
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((target, port))
            except Exception as e:
                self.log(f"[HATA] Baglanti {host}:{port} - {e}")
                client_socket.close()
                return

            if is_connect:
                client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                self.tunnel(client_socket, remote_socket, host)
            else:
                request = self.normalize_request(data, host)
                if self.is_blocked(host):
                    self.send_fragmented(remote_socket, request)
                else:
                    remote_socket.sendall(request)
                self.relay_to_client(remote_socket, client_socket)

            try:
                remote_socket.close()
            except Exception:
                pass

        except Exception as e:
            self.log(f"[HATA] Baglanti: {e}")
        finally:
            try:
                client_socket.close()
            except Exception:
                pass

    def tunnel(self, client_socket, remote_socket, host):
        blocked = self.is_blocked(host)
        stopped = threading.Event()

        def to_remote():
            try:
                while not stopped.is_set():
                    data = client_socket.recv(8192)
                    if not data:
                        break
                    if blocked:
                        self.send_fragmented(remote_socket, data)
                    else:
                        remote_socket.sendall(data)
            except Exception:
                pass
            finally:
                stopped.set()
                try:
                    remote_socket.shutdown(socket.SHUT_WR)
                except Exception:
                    pass

        threading.Thread(target=to_remote, daemon=True).start()

        try:
            while not stopped.is_set():
                data = remote_socket.recv(8192)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception:
            pass
        finally:
            stopped.set()
            try:
                client_socket.shutdown(socket.SHUT_WR)
            except Exception:
                pass

    def normalize_request(self, data, host):
        first_line = data.split(b"\r\n")[0]
        parts = first_line.split(b" ")
        if len(parts) >= 3:
            method = parts[0]
            target = parts[1]
            version = parts[2]
            if target.startswith(b"http://"):
                rest = target[7:]
                slash = rest.find(b"/")
                if slash == -1:
                    path = b"/"
                else:
                    path = rest[slash:]
                first_line = method + b" " + path + b" " + version
                return first_line + b"\r\n" + data.split(b"\r\n", 1)[1]
        return data

    def relay_to_client(self, remote_socket, client_socket):
        try:
            while True:
                data = remote_socket.recv(8192)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception:
            pass

    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(50)
        self.log(f"[BASLAT] Proxy port {self.port} - Mod: {self.mode}")
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(
                    target=self.handle_connection,
                    args=(client_socket, addr),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.log(f"[HATA] Accept: {e}")

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        self.log("[DURDU] Proxy kapatildi")


class KiwiBypassApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proxy_engine = ProxyEngine()
        self.proxy_engine.log_callback = self._on_log
        self.is_running = False
        self.log_lines = []
        self.config_file = Path("config.json")
        self.load_config()

    def build(self):
        self.theme_style = "Dark"
        self.theme_palette = "M3"
        Window.clearcolor = (0.04, 0.04, 0.06, 1)
        return Builder.load_string(KV)

    def on_start(self):
        self.load_domains_to_ui()
        self.update_dns_detail()

    def _on_log(self, msg):
        self.log_lines.append(msg)
        if len(self.log_lines) > 200:
            self.log_lines = self.log_lines[-200:]
        Clock.schedule_once(lambda dt: self._update_log_ui(msg), 0)

    def log(self, msg):
        self._on_log(msg)

    def _update_log_ui(self, msg):
        try:
            self.root.ids.log_text.text = "\n".join(self.log_lines[-50:])
        except Exception:
            pass

    def toggle_proxy(self):
        if self.is_running:
            self.stop_proxy()
        else:
            self.start_proxy()

    def start_proxy(self):
        try:
            self.proxy_engine.port = int(self.root.ids.detail_port.text)
            self.proxy_engine.start()
            self.is_running = True
            self.root.ids.status_indicator.md_bg_color = [0, 0.9, 0.46, 1]
            self.root.ids.status_text.text = "Aktif"
            self.root.ids.status_detail.text = f"Proxy calisiyor - port {self.proxy_engine.port}"
            self.root.ids.main_button_text.text = "DURDUR"
            self.log("[BASLATILDIM]")
        except Exception as e:
            self.log(f"[HATA] Baslatma: {e}")

    def stop_proxy(self):
        self.proxy_engine.stop()
        self.is_running = False
        self.root.ids.status_indicator.md_bg_color = [1, 0.09, 0.27, 1]
        self.root.ids.status_text.text = "Beklemede"
        self.root.ids.status_detail.text = "Proxy durakli"
        self.root.ids.main_button_text.text = "BASLAT"

    def switch_screen(self, name):
        self.root.ids.screen_manager.current = name

    def open_mod_menu(self):
        items = [
            {"text": k, "on_release": lambda x=k: self.set_mod(x)}
            for k in MODS.keys()
        ]
        self.mod_menu = MDDropdownMenu(
            caller=self.root.ids.mod_button,
            items=items,
        )
        self.mod_menu.open()

    def set_mod(self, name):
        self.proxy_engine.mode = MODS[name]
        self.root.ids.mod_text.text = name
        self.root.ids.detail_type.text = name
        menu = getattr(self, "mod_menu", None)
        if menu:
            menu.dismiss()
        self.log(f"[MOD] {name}")

    def open_dns_menu(self):
        items = [
            {"text": k, "on_release": lambda x=k: self.set_dns(x)}
            for k in DNS_SERVERS.keys()
        ]
        self.dns_menu = MDDropdownMenu(
            caller=self.root.ids.dns_button,
            items=items,
        )
        self.dns_menu.open()

    def set_dns(self, name):
        self.proxy_engine.dns_resolver.dns_server = DNS_SERVERS[name]
        self.root.ids.dns_text.text = name
        self.root.ids.detail_dns.text = f"{DNS_SERVERS[name]} ({name})"
        menu = getattr(self, "dns_menu", None)
        if menu:
            menu.dismiss()
        self.log(f"[DNS] {name} -> {DNS_SERVERS[name]}")

    def open_frag_menu(self):
        items = [
            {"text": k, "on_release": lambda x=k: self.set_frag(x)}
            for k in FRAG_SIZES.keys()
        ]
        self.frag_menu = MDDropdownMenu(
            caller=self.root.ids.frag_button,
            items=items,
        )
        self.frag_menu.open()

    def set_frag(self, name):
        mn, mx = FRAG_SIZES[name]
        self.proxy_engine.fragment_size_min = mn
        self.proxy_engine.fragment_size_max = mx
        self.root.ids.frag_text.text = name
        menu = getattr(self, "frag_menu", None)
        if menu:
            menu.dismiss()
        self.log(f"[FRAG] {mn}-{mx} byte")

    def toggle_auto_dns(self, active):
        self.proxy_engine.auto_dns = active
        self.log(f"[DNS] Otomatik: {'Acik' if active else 'Kapali'}")

    def save_custom_dns(self):
        ip = self.root.ids.custom_dns_field.text.strip()
        if ip:
            self.proxy_engine.dns_resolver.dns_server = ip
            self.root.ids.detail_dns.text = ip
            self.log(f"[DNS] Ozel: {ip}")

    def add_domain(self):
        domain = self.root.ids.add_domain_field.text.strip().lower()
        if domain and domain not in self.proxy_engine.blocked_domains:
            self.proxy_engine.blocked_domains.append(domain)
            self.root.ids.add_domain_field.text = ""
            self.load_domains_to_ui()
            self.log(f"[EKLENDI] {domain}")

    def remove_domain(self, domain):
        if domain in self.proxy_engine.blocked_domains:
            self.proxy_engine.blocked_domains.remove(domain)
            self.load_domains_to_ui()
            self.log(f"[SILINDI] {domain}")

    def reset_domains(self):
        self.proxy_engine.blocked_domains = list(DEFAULT_DOMAINS)
        self.load_domains_to_ui()
        self.log("[SIFIRLANDI] Varsayilan domainler yuklendi")

    def load_domains_to_ui(self):
        try:
            container = self.root.ids.domain_list
            container.clear_widgets()
            for d in self.proxy_engine.blocked_domains:
                card = MDCard(
                    size_hint_y=None,
                    height=dp(56),
                    radius=dp(12),
                    md_bg_color=[0.08, 0.08, 0.12, 1],
                    padding=[dp(12), dp(8)],
                )
                layout = MDBoxLayout(orientation="horizontal", spacing=dp(8))
                layout.add_widget(
                    MDLabel(
                        text=d,
                        font_style="Label",
                        role="medium",
                        theme_text_color="Custom",
                        text_color=[1, 1, 1, 1],
                        size_hint_x=0.75,
                        valign="center",
                    )
                )
                btn = MDButton(
                    style="text",
                    size_hint_x=0.25,
                    size_hint_y=None,
                    height=dp(40),
                    on_release=lambda inst, dom=d: self.remove_domain(dom),
                )
                btn.add_widget(
                    MDButtonIcon(
                        icon="delete",
                        theme_text_color="Custom",
                        text_color=[1, 0.09, 0.27, 1],
                    )
                )
                layout.add_widget(btn)
                card.add_widget(layout)
                container.add_widget(card)
            self.root.ids.detail_blocked.text = f"{len(self.proxy_engine.blocked_domains)} domain"
        except Exception:
            pass

    def update_dns_detail(self):
        try:
            ip = self.proxy_engine.dns_resolver.dns_server
            for name, server in DNS_SERVERS.items():
                if server == ip:
                    self.root.ids.detail_dns.text = f"{ip} ({name})"
                    self.root.ids.dns_text.text = name
                    return
            self.root.ids.detail_dns.text = ip
        except Exception:
            pass

    def clear_logs(self):
        self.log_lines.clear()
        self.root.ids.log_text.text = "Temizlendi..."

    def save_config(self):
        config = {
            "mode": self.proxy_engine.mode,
            "dns": self.proxy_engine.dns_resolver.dns_server,
            "frag_min": self.proxy_engine.fragment_size_min,
            "frag_max": self.proxy_engine.fragment_size_max,
            "port": self.proxy_engine.port,
            "domains": self.proxy_engine.blocked_domains,
            "auto_dns": self.proxy_engine.auto_dns,
        }
        try:
            self.config_file.write_text(json.dumps(config, indent=2))
        except Exception:
            pass

    def load_config(self):
        try:
            if self.config_file.exists():
                config = json.loads(self.config_file.read_text())
                self.proxy_engine.mode = config.get("mode", "dns_frag")
                self.proxy_engine.dns_resolver.dns_server = config.get("dns", "1.1.1.1")
                self.proxy_engine.fragment_size_min = config.get("frag_min", 2)
                self.proxy_engine.fragment_size_max = config.get("frag_max", 4)
                self.proxy_engine.port = config.get("port", 8888)
                self.proxy_engine.blocked_domains = config.get("domains", list(DEFAULT_DOMAINS))
                self.proxy_engine.auto_dns = config.get("auto_dns", True)
        except Exception:
            pass

    def on_stop(self):
        self.save_config()
        if self.is_running:
            self.proxy_engine.stop()


if __name__ == "__main__":
    KiwiBypassApp().run()
