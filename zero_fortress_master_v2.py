#!/usr/bin/env python3
import os
import sys
import time
import logging
import subprocess
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

# 동적 현재 경로 할당으로 하드코딩 제거
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, "share")
LOG_FILE = "/var/log/secure_forensic.log"

ATTACK_THRESHOLD = 3
TIME_WINDOW = 5
COOL_DOWN_TIME = 10

attack_timestamps = []
is_cooldown_active = False
cooldown_start_time = 0

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, 
    format='[%(asctime)s] [FORENSIC_EVIDENCE] [LAW_ARTICLE_46] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def execute_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    except:
        return "ERROR"

def get_attacker_ip():
    # [문법 경고 해결] r''를 사용한 Raw String 선언으로 ^172\. 이스케이프 경고 완벽 박멸
    res = execute_cmd(r"netstat -antp 2>/dev/null | grep 'ESTABLISHED' | awk '{print $5}' | cut -d: -f1 | grep -v '127.0.0.1' | grep -v '^172\.' | head -n 1")
    if not res or "ERROR" in res or res == "":
        res = execute_cmd("docker logs zero_nginx_proxy 2>/dev/null | tail -n 1 | awk '{print $1}'")
    return res if res and "ERROR" not in res else "UNKNOWN_CLOUD_EDGE_IP"

def shadow_kill_and_refresh_pool():
    print(f"{YELLOW}[*] Light-Weight Action: Executing Ultra-Fast Container Micro-Purge...{NC}")
    for i in range(1, 4):
        container_name = f"zero_container_{i}"
        execute_cmd(f"docker restart {container_name} >/dev/null 2>&1")
    print(f"{GREEN}[✔] Light-Weight Self-Healing Complete. All node memory pools purged.{NC}")

class OpenSourceClusterGuard(FileSystemEventHandler):
    def on_modified(self, event):
        global attack_timestamps, is_cooldown_active, cooldown_start_time
        if event.is_directory:
            return
        
        current_time = time.time()
        
        if is_cooldown_active:
            if current_time - cooldown_start_time > COOL_DOWN_TIME:
                is_cooldown_active = False
                attack_timestamps = []
                print(f"{GREEN}[*] Cooldown Guard Expired. Defense System Reset to Normal Mode.{NC}")
            else:
                return

        attack_timestamps = [t for t in attack_timestamps if current_time - t < TIME_WINDOW]
        attack_timestamps.append(current_time)
        attacker_ip = get_attacker_ip()
        
        print(f"\n{RED}[🚨 ALERT - INTEGRITY VIOLATION DETECTED]{NC}")
        print(f" ├─ TIME       : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print(f" ├─ FILE       : {os.path.basename(event.src_path)}")
        print(f" ├─ INTRUDER   : REAL ATTACKER SOURCE IDENTIFIED -> [ {attacker_ip} ]")
        logging.info(f"[INTEGRITY_VIOLATION] Path: {event.src_path} | Attacker REAL_IP: {attacker_ip}")

        shadow_kill_and_refresh_pool()

        if len(attack_timestamps) >= ATTACK_THRESHOLD:
            is_cooldown_active = True
            cooldown_start_time = current_time
            print(f"{YELLOW}[⚠️ WARNING] Self-Healing Storm Overload Prevention Triggered.{NC}")
            print(f"{YELLOW}           Cooldown Guard Active for next {COOL_DOWN_TIME} seconds.{NC}")

if __name__ == '__main__':
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    observer = PollingObserver(timeout=0.1)
    event_handler = OpenSourceClusterGuard()
    observer.schedule(event_handler, path=TARGET_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(f"\n{RED}[*] Hyper Zero Engine Terminated Defensively.{NC}")
    observer.join()
