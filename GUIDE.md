# Hyper Zero Architecture v2.5 - Deployment & Operations Guide

## 1. Prerequisites & Host Mapping (필수 조건 및 호스트 매핑)

Before deploying the isolated container pool, you must register the virtual container node addresses inside your local hosts table.
[KR] 격리된 컨테이너 풀을 배포하기 전에 로컬 hosts 테이블에 가상 컨테이너 노드 주소를 강제로 매핑해야 Nginx 프록시가 올바르게 라우팅할 수 있습니다.

```bash
# Map virtual container node names to local loopback address
# [KR] 로컬 루프백 주소에 가상 컨테이너 노드 주소 강제 매핑
echo "127.0.0.1 zero_container_1 zero_container_2 zero_container_3" | sudo tee -a /etc/hosts

# Install mandatory system dependencies
# [KR] 원터치 커널 및 보안 제어를 위한 필수 시스템 의존성 패키지 설치
sudo apt update && sudo apt install -y docker.io python3-pip net-tools iptables apache2-utils

# Install real-time directory monitoring library
# [KR] 0.1초 단위 실시간 무결성 감시(Watchdog)를 위한 파이썬 라이브러리 설치
pip3 install watchdog
```

---

## 2. Deployment & Core Execution (배포 및 핵심 방어 엔진 구동)

Inject the frontline Nginx reverse proxy configuration and execute the 68.2% shell-based integrated defense macro engine as a background daemon.
[KR] 최전선 Nginx 리버스 프록시 설정을 주입하고, 68.2% 쉘 기반의 원터치 통합 방어 엔진을 백그라운드 데몬 프로세스로 구동합니다.

```bash
# STEP 1: Copy Nginx configuration and verify syntax integrity
# [KR] Nginx 방어 프록시 설정을 복사하고 문법 무결성 검증 (정수 초 단위 최적화 반영)
sudo cp ./nginx_fortress_proxy.conf /etc/nginx/nginx.conf
sudo nginx -t

# STEP 2: Restart Nginx infrastructure service
# [KR] 컴파일 통과 확인 후 Nginx 인프라 서비스 재시작
sudo systemctl restart nginx

# STEP 3: Grant execute permission and run the integrated defense engine
# [KR] 통합 방어 스크립트에 실행 권한을 부여하고 백그라운드에서 상시 자동 구동
chmod +x ./run_all_defense.sh
nohup ./run_all_defense.sh > ./logs/defense_system.log 2>&1 &
```

---

## 3. Empirical Infrastructure Testing (실증적 인프라 보안 테스트)

Execute the following simulation benchmarks in a new terminal to validate the active defense layer.
[KR] 새 터미널을 열고 아래의 공격 시뮬레이션을 실행하여, 설계한 능동 방어 계층이 제대로 작동하는지 검증하십시오.

### 🧪 Attack Simulation A: L7 DDoS & Brute-Force Rate Limiting
Simulate high-volume concurrent requests targeting the proxy layer.
[KR] 프록시 계층에 대량의 동시 요청을 주입하여 자동화된 디도스(DDoS) 및 무차별 대입 공격 상황을 모사합니다.

```bash
# Inject 100 concurrent requests using ApacheBench to simulate a DDoS attack
# [KR] ApacheBench 도구를 활용해 초당 대량의 동시 요청 100개 강제 주입
ab -n 100 -c 10 http://127.0.0
```

*   **Expected Result (예상 결과):** Nginx blocks excessive aggressive requests (returning 503). Due to the structured `limit_req_zone` design, legitimate users can access `http://localhost/` seamlessly.
    [KR] Nginx가 공격성 요청을 칼같이 차단하고 503 오류를 반환합니다. 구조적인 로드 밸런싱 설계 덕분에 일반 사용자는 중단 없이 원활하게 서비스에 접속할 수 있습니다.

### 🧪 Attack Simulation B: WebShell Injection & Self-Healing Purge
Simulate a malicious intrusion where an attacker attempts to inject a webshell or tamper with core source codes inside the monitored directory.
[KR] 해커가 웹셸을 주입하거나 핵심 파일을 위변조하려는 악의적인 침입 상황을 시뮬레이션합니다.

```bash
# Simulate a webshell attack by forcing a tampered file into the monitored application directory
# [KR] 실시간 모니터링 중인 활성 디렉토리에 변조 파일 및 웹셸 강제 주입
echo "# HACKED_BY_ATTACKER" > ./src/protected_file.py
```

*   **Expected Result (예상 결과):** The 0.1s Python Watchdog engine instantly detects the integrity violation, triggers the crimson alert `[🚨 ALERT - INTEGRITY VIOLATION DETECTED]`, purges the compromised container node, and automatically rebuilds a pristine environment.
    [KR] 0.1초 단위의 파이썬 왓치독 엔진이 무결성 위반을 즉시 감지하여 `[🚨 ALERT - INTEGRITY VIOLATION DETECTED]` 빨간색 경고 배너를 터트립니다. 그와 동시에 해커가 장악한 도커 컨테이너 노드를 즉시 사살(Micro-Purge)하고 깨끗한 노드로 자동 자가 치유합니다. 세션은 독립형 Redis 브로커가 안전하게 유지합니다.

---

## 4. Maintenance & Operations Audit (운영 관리 및 무결성 검증)

Track live security automation states and verify infrastructure log integrity.
[KR] 상시 운영 중인 백그라운드 보안 프로세스의 상태를 점검하고, 인프라 로그의 무결성을 정밀 감사(Audit)합니다.

```bash
# Check running security daemons and verify PID states
# [KR] 현재 가동 중인 백어라운드 보안 데몬 프로세스의 PID 상태 확인
ps -ef | grep -E "run_all_defense|python3" | grep -v grep

# Verify operational log generation, file sizes, and integrity metrics
# [KR] 로그 디렉토리 내 파일들의 생성 상태, 크기, 무결성을 직관적으로 관리 및 검증
ls -al logs/
```

### 📱 Mobile Emergency Operations (모바일 긴급 장애 조치)
*   **Context:** In the absence of a workstation, critical configuration hotfixes (e.g., path refactoring for `*/log`) are handled directly via the GitHub web interface using a mobile Chrome browser.
    [KR] PC를 사용할 수 없는 외부 이동 중 긴급 경로 오류(`*/log`) 등이 발생했을 때, 스마트폰 모바일 크롬 브라우저로 깃허브 웹 인터페이스에 직접 접속하여 화면 제약을 극복하고 코드를 즉각 수정 및 커밋(Hotfix) 배포하여 상시 가용성을 보장합니다.

### 💾 Air-Gapped Physical Backup (하드웨어 무결성 동기화)
*   **Context:** Verified infrastructure configurations are synchronized to a physical, hardware-encrypted LUKS USB storage device mounted via `/media/sf_defense_share` to ensure comprehensive off-line disaster recovery.
    [KR] 가상머신 공유 폴더 마운트 통로를 개통하여 최종 검증된 Nginx 설정과 쉘 스크립트를 물리적인 LUKS 암호화 USB 저장소에 동기화합니다. 이를 통해 네트워크가 차단된 폐쇄망(Air-gapped) 환경에서도 완벽한 원상 복구가 가능한 '시스템-GitHub-물리저장소' 삼위일체 백업을 유지합니다.

---

## 5. Next-Generation Advanced Roadmap (차세대 아키텍처 로드맵)

*   **Kernel-Level Race Prevention via eBPF:** Transition from the current 100ms Python polling architecture to an Extended Berkeley Packet Filter (eBPF) model to hook kernel system calls (`sys_write`), blocking malicious file manipulation directly within the kernel space.
    [KR] 현재의 100ms 파이썬 폴링 구조에서 eBPF(Extended Berkeley Packet Filter) 모델로 전환하여 커널 시스템 호출(`sys_write`)을 직접 후킹하고, 커널 공간 내에서 악의적인 파일 조작을 원천 차단합니다.
*   **Fileless Memory Injection Shield:** Integrate CNCF runtime security profilers (e.g., Falco or KubeArmor) to detect and mitigate malicious runtime behaviors violating execution memory space.
    [KR] CNCF 런타임 보안 프로파일러(Falco 또는 KubeArmor 등)를 통합하여 실행 파일 없이 메모리 공간을 직접 변조하는 악의적인 런타임 침투 동작을 탐지하고 무력화합니다.
<img width="4000" height="3000" alt="6505" src="https://github.com/user-attachments/assets/9257d5e7-530f-43e0-be5d-887572f40963" />
