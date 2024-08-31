import re
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

import pymem
import scanmodule
import numpy as np
from ahk import AHK


@dataclass
class Monsters:
    large_monsters = {
        1: "Rathian",
        2: "Rathalos",
        3: "Khezu",
        4: "Basarios",
        5: "Gravios",
        7: "Diablos",
        8: "Yian Kut-ku",
        9: "Gypceros",
        10: "Plesioth",
        11: "Kirin",
        12: "Lao-Shan Lung",
        13: "Fatalis",
        14: "Velocidrome",
        15: "Gendrome",
        16: "Iodrome",
        17: "Cephadrome",
        18: "Yian Garuga",
        19: "Daimyo Hermitaur",
        20: "Shogun Ceanataur",
        21: "Congalala",
        22: "Blangonga",
        23: "Rajang",
        24: "Kushala Daora",
        25: "Chameleos",
        27: "Teostra",
        30: "Bulldrome",
        32: "Tigrex",
        33: "Akantor",
        34: "Giadrome",
        36: "Lavasioth",
        37: "Nargacuga",
        38: "Ukanlos",
        42: "Barioth",
        43: "Deviljho",
        44: "Barroth",
        45: "Uragaan",
        46: "Lagiacrus",
        47: "Royal Ludroth",
        49: "Agnaktor",
        50: "Alatreon",
        55: "Duramboros",
        56: "Niblesnarf",
        57: "Zinogre",
        58: "Amatsu",
        60: "Arzuros",
        61: "Lagombi",
        62: "Volvidon",
        63: "Brachydios",
        65: "Kecha Wacha",
        66: "Tetsucabra",
        67: "Zamtrios",
        68: "Najarala",
        69: "Seltas Queen",
        70: "Nerscylla",
        71: "Gore Magala",
        72: "Shagaru Magala",
        76: "Seltas",
        77: "Seregios",
        79: "Malfestio",
        80: "Glavenus",
        81: "Astalos",
        82: "Mizutsune",
        83: "Gammoth",
        84: "Nakarkos",
        85: "Great Maccao",
        86: "Valstrax",
        87: "Ahtal-Neset",
        88: "Ahtal-Ka",
        269: "Crimson Fatalis",
        513: "Gold Rathian",
        514: "Silver Rathalos",
        525: "White Fatalis",
        1025: "Dreadqueen Rathian",
        1026: "Dreadking Rathalos",
        1031: "Bloodbath Diablos",
        1042: "Deadeye Yian Garuga",
        1043: "Stonefist Hermitaur",
        1044: "Rustrazor Ceanataur",
        1056: "Grimclaw Tigrex",
        1061: "Silverwind Nargacuga",
        1069: "Crystalbeard Uragaan",
        1081: "Thunderlord Zinogre",
        1084: "Redhelm Arzuros",
        1085: "Snowbaron Lagombi",
        1090: "Drilltusk Tetsucabra",
        1103: "Nightcloak Malfestio",
        1104: "Hellblade Glavenus",
        1105: "Boltreaver Astalos",
        1106: "Soulseer Mizutsune",
        1107: "Elderfrost Gammoth",
        1303: "Furious Rajang",
        1323: "Savage Deviljho",
        1343: "Raging Brachydios",
        1351: "Chaotic Gore Magala",
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
                large_monster_results.append([name, hp, initial_hp])
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
            monster_names = {**Monsters.large_monsters, **Monsters.small_monsters}
            for monster in monsters:
                if monster[2] > 5:
                    print([monster_names[monster[0]], *monster[1::]])
        end = time.time()
        print(end - start)
    Test()
