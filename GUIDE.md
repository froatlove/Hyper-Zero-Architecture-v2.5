# 🛡️ Hyper Zero Architecture v2 - Complete Guide

> 누구나 따라 할 수 있는 실전 구축, AI Cloud DDoS 방어 & 테스트 매뉴얼  
> Easy-to-follow Deployment, AI Cloud DDoS Defense & Simulation Guide

---

## 1. ⚙️ 어떤 기반으로 만들어졌나요? (Background & Tech Stack)

이 시스템은 대규모 해킹 및 디도스(Zero-Day & DDoS Attack) 공격이 들어와 인프라 전체를 마비시키려 하거나 내부 파일을 변조할 때, 0.1초 만에 감지하여 해커가 장악한 노드를 사살(Shadow Kill)하고 트래픽을 원천 차단하는 AI Cloud 환경 최적화 무중단 자가 치유 아키텍처입니다.

### 🛠️ 핵심 기술 스택 (Core Tech Stack)
* Docker & Nginx: 웹 서비스를 3개의 컨테이너(Pool)로 분산 구동하며, Nginx가 앞단에서 트래픽을 안정적으로 밸런싱합니다.
* Independent Redis Broker: 컨테이너가 파괴되고 새로 켜지는 와중에도, 사용자의 로그인 상태(Session)를 안전하게 유지하는 영구 세션 저장소입니다.
* Python Watchdog (Polling 100ms): 파일의 미세한 변경 사항을 0.1초 단위로 정밀 감시하는 시스템의 '눈' 역할을 합니다.
* Linux Kernel Boost: 가혹한 공격 환경에서도 네트워크가 끊기지 않도록 리눅스 커널 소켓을 극한으로 튜닝했습니다.

---

## 2. 🛡️ AI Cloud DDoS 공격 방어 메커니즘 (DDoS Protection Layer)

본 시스템은 AI Cloud 인프라에 가해지는 다양한 레이어의 DDoS 공격을 계층별(Layered)로 방어하도록 설계되었습니다.

* L4 대용량 디도스 방어 (Kernel Level): 리눅스 커널 수준에서 `tcp_tw_reuse`, `somaxconn`, `tcp_max_syn_backlog`를 동적 조율하여, 해커가 좀비 PC로 싱크 플러딩(SYN Flooding) 공격을 퍼부어 소켓을 고갈시키려 해도 AI Cloud 노드가 대규모 동시 접속을 버텨냅니다.
* L7 웹 디도스 및 고빈도 요청 차단 (iptables Hashlimit): 
  `run_all_defense.sh` 내부의 `hashlimit` 방어 규칙이 작동합니다. 단일 IP가 초당 60회(`--hashlimit-upto 60/sec`) 이상의 비정상적인 폭풍 요청을 보내면, 시스템 버스트 한도(15회) 초과 즉시 해당 IP로부터의 모든 접속을 물리적으로 DROP(드롭) 시켜 인프라 진입을 차단합니다.
* 자가 치유 폭풍 과부하 방지 (Storm Control Cooldown): 디도스 공격으로 인해 컨테이너가 무한히 파괴되고 재생성되면서 시스템 자원(CPU/메모리)이 고갈되는 '자가 치유 폭풍 폭주' 현상을 방어하기 위해, 임계치 초과 시 10초간 제어 모드를 강제 동결하는 쿨다운 가드가 작동합니다.

---

## 3. 📦 무엇을 설치해야 하나요? (Prerequisites)

시스템 가동을 위해 리눅스(Linux OS) 환경에서 딱 두 가지만 준비해 주세요.

### ① 시스템 패키지 설치 (System Packages)
```bash
# Docker 및 Docker 컴포즈 설치
sudo apt update && sudo apt install -y docker.io python3-pip

# 네트워크 모니터링 및 방화벽 툴 설치 (DDoS IP 추적 및 차단용)
sudo apt install -y net-tools iptables
```

### ② 파이썬 감시 라이브러리 설치 (Python Library)
```bash
# 파일 변조 실시간 감지를 위한 watchdog 패키지 설치
pip3 install watchdog
```

---

## 4. 🚀 어떻게 실행하나요? (How to Run)

모든 디도스 방화벽 빌드, 커널 최적화, 인프라 구축이 스크립트 한 줄로 자동 진행됩니다.

```bash
# 1. 스크립트 실행 권한 부여 (Give Execution Permission)
chmod +x run_all_defense.sh

# 2. 마스터 관리자 권한으로 시스템 기동 (Run with Root Privileges)
sudo ./run_all_defense.sh
```
* Note: 실행 직후 터미널 창은 외부 명령 오동작 및 우회 침투를 막기 위해 보안 관제 락(Foreground Monitor Lock) 상태로 고정됩니다. 정상적인 현상이니 그대로 켜두세요!

---

## 5. 🧪 테스트는 어떻게 하나요? (Detailed Testing & Simulation)

관제 터미널을 그대로 둔 상태에서, **새 터미널 창(New Terminal)**을 열고 아래 시뮬레이션을 차례대로 수행하며 성능을 검증합니다.

### 🔍 [Step 1] 가동 상태 체크 (Health Check)
```bash
# 컨테이너 5개가 정상 가동 중인지 확인
docker ps

# 서비스 정상 응답 및 로드밸런싱 확인
curl http://localhost
```

### ⚡ [Step 2] L7 HTTP 디도스(DDoS) 공격 및 자동 격리 테스트
단일 가상 노드에서 서비스가 다운될 때까지 무차별 대량 트래픽 요청(DDoS 폭격)을 보냅니다.
```bash
# 1초에 수백 번의 HTTP 요청을 무한 반복하는 공격 스크립트 실행
while true; do curl -s -o /dev/null http://localhost; done
```
* 💥 기대 결과 (Expected Result): 
  초반 수십 개의 요청 이후, `iptables hashlimit` 규칙에 의해 공격자 IP가 방화벽에 완전히 걸려들어 트래픽이 공중 분해(DROP)됩니다. 공격 창에서는 요청이 끊기거나 먹통(Timeout)이 되지만, 외부의 정상적인 다른 사용자가 `http://localhost`에 접속하면 클러스터 풀이 완벽히 살아있어 정상적으로 웹 페이지가 열리는 DDoS 격리 방어를 눈으로 확인할 수 있습니다.

### 🦹 [Step 3] 웹셸 소스코드 변조 공격 시뮬레이션 (Integrity Attack)
해커가 웹 서버의 소스코드를 강제로 수정(변조)했다고 가정하고 파일을 건드려 봅니다.
```bash
echo "# HACKED_BY_ATTACKER" >> /media/sf_defense_share/protected_file.py
```
* 💥 기대 결과 (Expected Result): 
  원래 터미널 창에 즉시 `[🚨 ALERT - INTEGRITY VIOLATION DETECTED]` 경고가 뜨며 침입자 IP를 잡아냅니다. 그와 동시에 변조된 컨테이너는 즉시 사살되고 새 컨테이너로 교체됩니다 (`docker ps`로 컨테이너 가동시간 초기화 확인 가능).

---

## 📄 6. 핵심 요약 (Summary Checklist)

1. 실행법: `sudo ./run_all_defense.sh` 실행 후 터미널 관제창 유지.
2. DDoS 방어: Kernel 소켓 가속 튜닝 + `iptables hashlimit` 기반 초당 요청 제한으로 폭격 트래픽 드롭.
3. 작동 원리: 대용량 디도스 인프라 격리 차단 ➡️ 소스 변조 감지 ➡️ 0.1초 만에 컨테이너 즉시 사살 및 리빌드 ➡️ 그 와중에도 사용자의 로그인(Redis)은 완벽 유지.
4. 증적 확보: 모든 공격 및 방어 내역은 국내 정보통신망법 제46조에 의거하여 `/var/log/secure_forensic.log` 장부에 영구 박제됩니다.
---

## 🔮 7. 향후 고도화 로드맵 (Future Roadmap & Production Scale)

본 v2.5 아키텍처는 단일 호스트 가상화 샌드박스(Single-Host Sandbox) 환경에서 최고 수준의 결함 보완과 무중단 자가 치유를 증명했습니다. 향후 엔터프라이즈급 AI 클라우드 런타임 환경으로 확장하기 위한 3대 차세대 기술 고도화 로드맵은 다음과 같습니다.

### ① 커널 시스템 콜 레벨 파일 런타임 격리 (Anti-Race Condition via eBPF)
*   **현 시점의 한계 (Constraint)**: 현재의 100ms 정밀 PollingObserver 방식은 초고속 자동화 공격 시나리오에서 미세한 타임윈도우 틈새를 노린 경합 조건(Race Condition) 공격에 일시적으로 노출될 잠재적 위험이 존재합니다.
*   **고도화 방향 (Roadmap)**: 유저 공간(User-space)에서의 주기적 스캔 한계를 극복하기 위해, 리눅스 커널 커스텀 모듈 또는 **eBPF(Extended Berkeley Packet Filter)** 기술을 도입합니다. 파일 쓰기(`sys_write`) 시스템 콜이 커널 영역에서 접수되는 즉시 프로세스를 블로킹(Blocking) 및 격리하는 동적 인라인 차단 메커니즘을 결합할 예정입니다.

### ② 파일리스(Fileless) 메모리 인젝션 방어 (Runtime Process Profiling)
*   **현 시점의 한계 (Constraint)**: 스토리지 레이어의 물리적 소스코드 변조 무결성은 완벽히 보장하지만, 디스크 파일은 건드리지 않고 구동 중인 Python 프로세스의 가상 메모리 주소 공간을 직접 오염시키는 메모리 변조(Memory Injection) 및 파일리스(Fileless) 공격 유형은 인지하기 어렵습니다.
*   **고도화 방향 (Roadmap)**: 파일 무결성 모니터링(FIM)을 넘어, 백엔드 컨테이너의 실시간 메모리 해시(Memory Hash) 검증 및 실행 프로세스의 런타임 동작 궤적을 프로파일링하는 **CWPP(Cloud Workload Protection Platform)** 기술(예: KubeArmor, Falco)을 클러스터에 동기화할 계획입니다.

### ③ 역프록시 단일 장애점(SPOF) 제거 및 클라우드 가상 외곽 방어 (Cloud-Native Traffic Scrubbing)
*   **현 시점의 한계 (Constraint)**: 백엔드 노드 풀은 다중화 가용성을 확보했으나, 대용량 DDoS 트래픽을 정면으로 수용하는 `zero_nginx_proxy` 컨테이너가 단일 인스턴스로 구동되어 역프록시 계층 자체가 단일 장애점(SPOF, Single Point of Failure)이 될 수 있습니다.
*   **고도화 방향 (Roadmap)**: 단일 호스트 인프라의 `iptables` 필터링 용량 한계를 탈피하고, AWS ALB(Application Load Balancer) 멀티 가용 영역(AZ) 배치 및 **Cloudflare Magic Transit / AWS Shield Advanced**와 같은 대규모 애니캐스트(Anycast) 기반의 외곽 스크러빙 센터(Scrubbing Center) 연동 구조를 설계하여 L4/L7 폭격 트래픽을 인프라 진입 전 단계에서 선제 소거하는 아키텍처 확장을 추진 중입니다.

