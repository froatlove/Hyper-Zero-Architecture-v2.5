# 🛡️ Hyper-Zero Architecture v2.5 - Deployment & Testing
> **Automated Self-Healing & AI Cloud DDoS Protection Infrastructure**

---

## 🟥 1. Prerequisites & Hostname Mapping
Before deploying the isolated container pool (`zero_backend_pool`), you must register the virtual node addresses in the host network table.

```bash
# [KO] 로컬 루프백 주소에 가상 컨테이너 노드 이름 매핑
echo "127.0.0.1 zero_container_1 zero_container_2 zero_container_3" >> /etc/hosts
```

### Required Packages
```bash
# [KO] 필수 시스템 의존성 패키지 설치
sudo apt update && sudo apt install -y docker.io python3-pip net-tools iptables apache2-utils

# [KO] 실시간 디렉토리 감시 파이썬 라이브러리 설치
pip3 install watchdog
```

---

## 🟦 2. Deployment & Usage
Inject the frontline Nginx reverse proxy config and run the 68.2% shell-based integrated defense macro engine into the background daemon.

```bash
# [STEP 1] Copy Nginx configuration and verify syntax integrity
cp ./nginx_fortress_proxy.conf /etc/nginx/nginx.conf
nginx -t

# [STEP 2] Restart Nginx infrastructure service
systemctl restart nginx

# [STEP 3] Grant execute permission and run the integrated defense script
chmod +x ./run_all_defense.sh
cp ./run_all_defense.sh /usr/local/bin/run_all_defense
nohup /usr/local/bin/run_all_defense > /var/log/defense_system.log 2>&1 &
```

---

## 🟩 3. Empirical Infrastructure Testing
Open a **New Terminal** and run the following simulation benchmarks to verify the active defense layers.

### 🧪 Test A: L7 DDoS & Brute-Force Rate-Limiting
Simulate an automated scanner or brute-force attack flooding the proxy with high requests.
```bash
# [KO] ApacheBench 도구를 활용해 초당 대량의 동시 요청 100개 주입 (디도스 모사)
ab -n 100 -c 10 http://127.0.0
```
* **Expected Result:** Nginx drops consecutive aggressive requests using `limit_req_zone` (Returning 503). Normal users can still access `http://localhost/` flawlessly without interruption due to the structural load-balancing design.

### 🧪 Test B: WebShell Injection & Self-Healing Purge
Simulate a malicious breach where a hacker attempts to inject a WebShell or temper core files.
```bash
# [KO] 가상의 웹 서비스 공유 디렉토리에 변조 파일 강제 주입 (공격 모사)
echo "# HACKED_BY_ATTACKER" > /media/sf_defense_share/share/protected_file.py
```
* **Expected Result:** The 100ms Python Watchdog polling engine immediately intercepts the integrity violation, triggers `[ 🚨 ALERT - INTEGRITY VIOLATION DETECTED ]`, purges the compromised node, and automatically rebuilds a clean container node.

---

## 🟨 4. Monitoring & Forensics Verification
Trace live background processes and real-time security automation auditing logs.

```bash
# Check running security daemons (PID Verification)
ps -ef | grep -E "run_all_defense|python3|zero_fortress" | grep -v grep

# Track live security detection and container healing logs
tail -f /var/log/defense_system.log
```

---

## 🚀 5. Advanced Next-Gen Architecture Roadmap
* **Kernel-Level Anti-Race via eBPF:** Transitioning from the current 100ms Python polling architecture to **eBPF (Extended Berkeley Packet Filter)** to hook kernel system calls (`sys_write`), blocking malicious file manipulation directly within the kernel layer.
* **Fileless Memory Injection Shield:** Integrating CNCF runtime security profilers (e.g., Falco / KubeArmor) to detect and mitigate malicious runtime behavioral traits tampering with execution memory spaces.
