import re
import time
from struct import unpack
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

import pymem
import scanmodule
import numpy as np
from ahk import AHK


@dataclass
class Monsters:
    large_monsters = {
        1: {
            "name": "Rathian",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        2: {
            "name": "Rathalos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        3: {
            "name": "Khezu",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        4: {
            "name": "Basarios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        5: {
            "name": "Gravios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        7: {
            "name": "Diablos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        8: {
            "name": "Yian Kut-ku",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        9: {
            "name": "Gypceros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        10: {
            "name": "Plesioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        11: {
            "name": "Kirin",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        12: {
            "name": "Lao-Shan Lung",
            "crowns": {"g": None, "s": None, "m": None}
        },
        13: {
            "name": "Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        14: {
            "name": "Velocidrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        15: {
            "name": "Gendrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        16: {
            "name": "Iodrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        17: {
            "name": "Cephadrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        18: {
            "name": "Yian Garuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        19: {
            "name": "Daimyo Hermitaur",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        20: {
            "name": "Shogun Ceanataur",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        21: {
            "name": "Congalala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        22: {
            "name": "Blangonga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        23: {
            "name": "Rajang",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        24: {
            "name": "Kushala Daora",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        25: {
            "name": "Chameleos",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        27: {
            "name": "Teostra",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        30: {
            "name": "Bulldrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        32: {
            "name": "Tigrex",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        33: {
            "name": "Akantor",
            "crowns": {"g": None, "s": None, "m": None}
        },
        34: {
            "name": "Giadrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        36: {
            "name": "Lavasioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        37: {
            "name": "Nargacuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        38: {
            "name": "Ukanlos",
            "crowns": {"g": None, "s": None, "m": None}
        },
        42: {
            "name": "Barioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        43: {
            "name": "Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        44: {
            "name": "Barroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        45: {
            "name": "Uragaan",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        46: {
            "name": "Lagiacrus",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        47: {
            "name": "Royal Ludroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        49: {
            "name": "Agnaktor",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        50: {
            "name": "Alatreon",
            "crowns": {"g": None, "s": None, "m": None}
        },
        55: {
            "name": "Duramboros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        56: {
            "name": "Niblesnarf",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        57: {
            "name": "Zinogre",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        58: {
            "name": "Amatsu",
            "crowns": {"g": None, "s": None, "m": None}
        },
        60: {
            "name": "Arzuros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        61: {
            "name": "Lagombi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        62: {
            "name": "Volvidon",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        63: {
            "name": "Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        65: {
            "name": "Kecha Wacha",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        66: {
            "name": "Tetsucabra",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        67: {
            "name": "Zamtrios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        68: {
            "name": "Najarala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        69: {
            "name": "Seltas Queen",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        70: {
            "name": "Nerscylla",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        71: {
            "name": "Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        72: {
            "name": "Shagaru Magala",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        76: {
            "name": "Seltas",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        77: {
            "name": "Seregios",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        79: {
            "name": "Malfestio",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        80: {
            "name": "Glavenus",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        81: {
            "name": "Astalos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        82: {
            "name": "Mizutsune",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        83: {
            "name": "Gammoth",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        84: {
            "name": "Nakarkos",
            "crowns": {"g": None, "s": None, "m": None}
        },
        85: {
            "name": "Great Maccao",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        86: {
            "name": "Valstrax",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        87: {
            "name": "Ahtal-Neset",
            "crowns": {"g": None, "s": None, "m": None}
        },
        88: {
            "name": "Ahtal-Ka",
            "crowns": {"g": None, "s": None, "m": None}
        },
        269: {
            "name": "Crimson Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        513: {
            "name": "Gold Rathian",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        514: {
            "name": "Silver Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        525: {
            "name": "White Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        1025: {
            "name": "Dreadqueen Rathian",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1026: {
            "name": "Dreadking Rathalos",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1031: {
            "name": "Bloodbath Diablos",
            "crowns": {"g": 114, "s": 110, "m": 96}
        },
        1042: {
            "name": "Deadeye Yian Garuga",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1043: {
            "name": "Stonefist Hermitaur",
            "crowns": {"g": 119, "s": 114, "m": 97}
        },
        1044: {
            "name": "Rustrazor Ceanataur",
            "crowns": {"g": 114, "s": 110, "m": 96}
        },
        1056: {
            "name": "Grimclaw Tigrex",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1061: {
            "name": "Silverwind Nargacuga",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1069: {
            "name": "Crystalbeard Uragaan",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1081: {
            "name": "Thunderlord Zinogre",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1084: {
            "name": "Redhelm Arzuros",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1085: {
            "name": "Snowbaron Lagombi",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1090: {
            "name": "Drilltusk Tetsucabra",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1103: {
            "name": "Nightcloak Malfestio",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1104: {
            "name": "Hellblade Glavenus",
            "crowns": {"g": 119, "s": 114, "m": 97}
        },
        1105: {
            "name": "Boltreaver Astalos",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1106: {
            "name": "Soulseer Mizutsune",
            "crowns": {"g": 114, "s": 110, "m": 97}
        },
        1107: {
            "name": "Elderfrost Gammoth",
            "crowns": {"g": 114, "s": 110, "m": 97}
        },
        1303: {
            "name": "Furious Rajang",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        1323: {
            "name": "Savage Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        1343: {
            "name": "Raging Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        1351: {
            "name": "Chaotic Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
    }

    small_monsters = {
        4097: "Aptonoth",
        4098: "Apceros",
        4099: "Kelbi",
        4100: "Mosswine",
        4101: "Hornetaur",
        4102: "Vespoid",
        4103: "Felyne",
        4104: "Melynx",
        4105: "Velociprey",
        4106: "Genprey",
        4107: "Ioprey",
        4108: "Cephalos",
        4109: "Bullfango",
        4110: "Popo",
        4111: "Giaprey",
        4112: "Anteka",
        4113: "Great Thunderbug",
        4115: "Remobra",
        4116: "Hermitaur",
        4117: "Ceanataur",
        4118: "Conga",
        4119: "Blango",
        4121: "Rhenophlos",
        4122: "Bnahabra",
        4123: "Altaroth",
        4130: "Jaggi",
        4131: "Jaggia",
        4135: "Ludroth",
        4136: "Uroktor",
        4137: "Slagtoth",
        4138: "Gargwa",
        4140: "Zamite",
        4141: "Konchu",
        4142: "Maccao",
        4143: "Larinoth",
        4144: "Moofah",
        4197: "Rock",
    }


def read_int(process_handle, address, length=2):
    return int.from_bytes(pymem.memory.read_bytes(process_handle, address, length), 'little')


def read_float(process_handle, address, length=4):
    return unpack('<f', pymem.memory.read_bytes(process_handle, address, length))[0]


def scan_aob_batched(
        process_handle,
        base_address,
        pattern, scan_size,
        show_small_monsters,
        num_chunks=400,
        max_workers=2
):
    large_monster_results = []
    small_monster_results = []
    try:
        wildcard = "??"
        bytes_pattern = bytes(int(byte, 16) if byte != wildcard else 0x00 for byte in pattern.split())
        pattern_np = np.frombuffer(bytes_pattern, dtype=np.uint8)
        mask = np.array([0xFF if byte != wildcard else 0x00 for byte in pattern.split()], dtype=np.uint8)
        chunk_size = scan_size // num_chunks

        large_monsters = Monsters.large_monsters
        small_monsters = Monsters.small_monsters if show_small_monsters else {}

        results = []
        with ThreadPoolExecutor(max_workers) as executor:
            futures = []
            for i in range(num_chunks):
                chunk_offset = i * chunk_size
                memory_chunk = pymem.memory.read_bytes(process_handle, base_address + chunk_offset, chunk_size)
                futures.append(
                    executor.submit(scanmodule.scan_chunk, memory_chunk, pattern_np, mask, base_address, chunk_offset)
                )

            for future in as_completed(futures):
                results.extend(future.result())

        results.sort(key=lambda x: x[0])

        for result in results:
            name = read_int(process_handle, result[0])
            hp = read_int(process_handle, result[1])
            initial_hp = read_int(process_handle, result[2])
            monster_name = large_monsters.get(name)
            if monster_name:
                monster_size = int(round(read_float(process_handle, result[1] - 0x1C0) * 100, 2))
                large_monster_results.append([name, hp, initial_hp, monster_size])
            elif show_small_monsters:
                monster_name = small_monsters.get(name)
                if monster_name:
                    small_monster_results.append([name, hp, initial_hp])
    except (Exception,):
        pass
    return large_monster_results + small_monster_results


def get_base_address(process_name):
    if process_name.lower() == "ryujinx.exe":
        region_address = scanmodule.get_regions(process_name, 0xE955000)
        if region_address:
            return region_address + 0x4052000
        return None
    region_address = scanmodule.get_regions(process_name, 0x9BBF000)
    if not region_address:
        region_address = scanmodule.get_regions(process_name, 0x9BAE000)
    return region_address


def get_data(pid, base_address, only_large_monsters, workers=2):
    process_handle = pymem.process.open(pid)
    pattern = "?? ?? 01 ?? 0F 18 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 20 00 00 00 00 00 00 00"
    scan_size = 0x6000000  # 0x9BBF000 or 7BBF000
    if process_handle:
        return scan_aob_batched(
            process_handle, base_address, pattern, scan_size, only_large_monsters, max_workers=workers
        )
    else:
        return []


if __name__ == "__main__":
    class Test:
        start = time.time()
        ahk = AHK(version="v2")
        target_window_title = "MONSTER HUNTER (GENERATIONS ULTIMATE|XX Nintendo Switch Ver.)[\\w\\W\\s]+"
        not_responding_title = " \\([\\w\\s]+\\)$"
        yuzu_target_window_title = "(yuzu|suyu)[\\w\\W\\s]+\\| (HEAD|dev)-[\\w\\W\\s]+"
        win = None
        is_xx = False
        base_address = None
        not_responding = ahk.find_window(
            title=target_window_title + not_responding_title, title_match_mode="RegEx"
        )
        if not not_responding:
            win = ahk.find_window(title=target_window_title, title_match_mode="RegEx")
            if win:
                if re.search("XX", win.title):
                    is_xx = True
                not_responding2 = ahk.find_window(
                    title=yuzu_target_window_title + not_responding_title, title_match_mode="RegEx"
                )
                if not not_responding2:
                    win2 = ahk.find_window(title=yuzu_target_window_title, title_match_mode="RegEx")
                    if win2:
                        win = win2
        if win:
            base_address = get_base_address(win.process_name)
            monsters = get_data(win.pid, base_address, True)
            for monster in monsters:
                if monster[2] > 5:
                    large_monster = Monsters.large_monsters.get(monster[0])
                    small_monster_name = Monsters.small_monsters.get(monster[0])
                    if large_monster:
                        print([large_monster["name"], *monster[1::]])
                    if small_monster_name:
                        print([small_monster_name, *monster[1::]])
        end = time.time()
        print(end - start)
    Test()
