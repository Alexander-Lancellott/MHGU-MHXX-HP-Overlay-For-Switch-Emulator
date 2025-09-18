import re
import time
from math import ceil
from struct import unpack
from concurrent.futures import ThreadPoolExecutor, as_completed

import pymem
import scanmodule
import numpy as np
from ahk import AHK
from modules.models import Monsters


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

        results.sort(key=lambda x: read_int(process_handle, x[1] - 0x450))

        for result in results:
            name = read_int(process_handle, result[0])
            hp = read_int(process_handle, result[1])
            initial_hp = read_int(process_handle, result[2])
            is_visible = read_int(process_handle, result[1] - 0x17A0, 1) != 0x7 or hp != 0x0
            if large_monsters.get(name) and is_visible:
                pointer = result[1]
                monster_size = int(round(read_float(process_handle, result[1] - 0x1C0) * 100, 2))
                abnormal_status = {}

                def add_abnormal_status(status_name: str, values: list):
                    if values[1] != 0xFFFF:
                        abnormal_status.update({
                            status_name: values,
                        })

                add_abnormal_status("Poison", [
                    read_int(process_handle, pointer + 0x5924, 2),
                    read_int(process_handle, pointer + 0x5930, 2)
                ])
                add_abnormal_status("Sleep", [
                    read_int(process_handle, pointer + 0x5928, 2),
                    read_int(process_handle, pointer + 0x5926, 2)
                ])
                add_abnormal_status("Paralysis", [
                    read_int(process_handle, pointer + 0x593E, 2),
                    read_int(process_handle, pointer + 0x593C, 2)
                ])
                add_abnormal_status("Dizzy", [
                    read_int(process_handle, pointer + 0x5A06, 2),
                    read_int(process_handle, pointer + 0x5A08, 2)
                ])
                add_abnormal_status("Exhaust", [
                    read_int(process_handle, pointer + 0x5A12, 2),
                    read_int(process_handle, pointer + 0x5A14, 2)
                ])
                add_abnormal_status("Jump", [
                    read_int(process_handle, pointer + 0x5A2A, 2),
                    read_int(process_handle, pointer + 0x5A2C, 2)
                ])
                add_abnormal_status("Blast", [
                    read_int(process_handle, pointer + 0x5A3A, 2),
                    read_int(process_handle, pointer + 0x5A38, 2)
                ])
                abnormal_status.update({
                    "Rage": int(ceil(
                        read_float(process_handle, pointer + 0x1A4) / 60
                    ))
                })
                large_monster_results.append([name, hp, initial_hp, monster_size, abnormal_status, pointer])

            elif small_monsters.get(name) and show_small_monsters and is_visible:
                monster_name = small_monsters.get(name)
                if monster_name:
                    small_monster_results.append([name, hp, initial_hp])
    except (Exception,):
        pass

    return {
        "monsters": large_monster_results + small_monster_results,
        "total": [len(large_monster_results), len(small_monster_results)],
    }


def get_monster_selected(
        pid,
        start_address,
        num_chunks=400,
        max_workers=2
):
    base_address = start_address
    process_handle = pymem.process.open(pid)
    pattern = "28 00 00 00 D1"
    scan_size = 0x5000000

    wildcard = "??"
    bytes_pattern = bytes(int(byte, 16) if byte != wildcard else 0x00 for byte in pattern.split())
    pattern_np = np.frombuffer(bytes_pattern, dtype=np.uint8)
    mask = np.array([0xFF if byte != wildcard else 0x00 for byte in pattern.split()], dtype=np.uint8)
    chunk_size = scan_size // num_chunks

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

    if len(results) > 0:
        return read_int(process_handle, results[0][1] - 0x175D, 1)
    return 0


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
    pattern = "?? ?? 01 ?? ?? 18 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 20 00 00 00 00 00 00 00"
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
        target_window_title = (
            r"(MONSTER HUNTER (GENERATIONS ULTIMATE|XX Nintendo Switch Ver.)|"
            r"\(0100C3800049C000\)|\(0100770008DD8000\))[\w\W\s]+"
        )
        not_responding_title = r" \([\w\s]+\)$"
        yuzu_target_window_title = r"(yuzu|suyu)[\w\W\s]+\| (HEAD|dev)-[\w\W\s]+"
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
            data = get_data(win.pid, base_address, True)
            monster_selected = get_monster_selected(win.pid, base_address)
            monsters = data["monsters"]
            print("base_address:", hex(base_address))
            for monster in monsters:
                if monster[2] > 5:
                    large_monster = Monsters.large_monsters.get(monster[0])
                    small_monster_name = Monsters.small_monsters.get(monster[0])
                    if large_monster:
                        print([large_monster["name"], *monster[1::], monster_selected])
                    if small_monster_name:
                        print([small_monster_name, *monster[1::]])
        end = time.time()
        print(end - start)
    Test()
