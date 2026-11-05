# 🛡️ Hyper Zero Architecture v2

> **Kernel-Level Monolithic Defense & Self-Healing Cluster System**  
> 대규모 제로데이 인프라 타격 상황에서 서비스 무중단성(High Availability)과 데이터 침해 증적을 실시간으로 확보하기 위해 설계된 커널 가속형 자가 치유 아키텍처입니다.

---

## ✨ Key Features

- **Self-Healing Storm Cooldown Guard**
  - 단시간 내 700인 이상의 분산 침투 또는 고빈도 웹셸 변조 공격 시 발생하는 컨테이너 재생성 폭풍(Overload)을 제어하는 임계치 기반 쿨다운 가드 탑재.
- **Nginx & Kernel Socket Optimization**
  - `net.ipv4.tcp_tw_reuse`, `somaxconn`, `max_syn_backlog` 등 하이 레벨 커널 매개변수 동적 튜닝 및 Nginx Keepalive 가속을 통해 대규모 공격 시 접속 단절 증상을 박멸.
- **Independent Redis Session Broker**
  - 백엔드 컨테이너 풀이 침해로 인해 파괴 및 동적 재생성되는 과정에서도 사용자의 세션 및 로그인 인프라를 100% 무중단 유지.
- **VirtualBox Polling Observer Bypass**
  - VirtualBox 공유 폴더 특성상의 `inotify` 이벤트 차단 한계를 극복하기 위해 `watchdog` 엔진을 100ms 정밀 폴링 상태로 커스텀 튜닝.
- **Foreground Infinite Monitor Lock**
  - 터미널 포그라운드를 완벽하게 장악하여 불필요한 명령어 입력 취약점 침투 경로를 사전에 차단하는 보안 대시보드 시스템.

---

## 🏗️ Architecture Design

```text
[ External Attacker ] 
       │ (iptables Hashlimit / Drop Protection)
       ▼
 ┌───────────┐ Keepalive 64  ┌────────────────────────┐
 │   Nginx   │ ────────────> │ zero_container_1 (8080)│ ──┐
 │  Reverse  │               ├────────────────────────┤   │ 
 │   Proxy   │               │ zero_container_2 (8080)│   ├──> [ Redis Session Broker ]
 └───────────┘               ├────────────────────────┤   │    (Session Data Is Safe!)
                             │ zero_container_3 (8080)│ ──┘
                             └────────────────────────┘
                                         ▲
  ┌──────────────────────────────────────┘ (Shadow Kill & Auto Restarter)
  │
┌──────────────────────────────┐
│  zero_fortress_master_v2.py  │ <── [ PollingObserver (100ms) Watchdog ]
└──────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Linux Environment (Ubuntu / CentOS 권장)
- Docker & Docker-compose
- Python 3.x & `watchdog` 라이브러리 (`pip install watchdog`)

### 2. Deployment
본 아키텍처는 제어기 실행 한 번으로 커널 최적화, 네트워크 브릿지 생성, 분산 프록시 풀 빌드를 논스톱으로 처리합니다.

```bash
# 1. 저장소 복사
git clone https://github.com
cd hyper-zero-architecture

# 2. 실행 권한 부여 및 마스터 클러스터 가동
chmod +x run_all_defense.sh
sudo ./run_all_defense.sh
```

### 3. Log Compliance
모든 탐지 증적과 침입 추적 데이터는 **정보통신망 이용촉진 및 정보보호 등에 관한 법률 제46조(정보통신망의 안정성 확보 등)** 기준을 준수하여 물리 로그 장부에 즉시 영구 기록됩니다.
```bash
tail -f /var/log/secure_forensic.log
```

---

## 📜 License
This project is open-source tested under the MIT License.
# 🛡️ Hyper Zero Architecture v2

> **Kernel-Level Monolithic Defense & Self-Healing Cluster System**  
> 대규모 제로데이 인프라 타격 상황에서 서비스 무중단성(High Availability)과 데이터 침해 증적을 실시간으로 확보하기 위해 설계된 커널 가속형 자가 치유 아키텍처입니다.

---

## ✨ Key Features

- **Self-Healing Storm Cooldown Guard**
  - 단시간 내 700인 이상의 분산 침투 또는 고빈도 웹셸 변조 공격 시 발생하는 컨테이너 재생성 폭풍(Overload)을 제어하는 임계치 기반 쿨다운 가드 탑재.
- **Nginx & Kernel Socket Optimization**
  - `net.ipv4.tcp_tw_reuse`, `somaxconn`, `max_syn_backlog` 등 하이 레벨 커널 매개변수 동적 튜닝 및 Nginx Keepalive 가속을 통해 대규모 공격 시 접속 단절 증상을 박멸.
- **Independent Redis Session Broker**
  - 백엔드 컨테이너 풀이 침해로 인해 파괴 및 동적 재생성되는 과정에서도 사용자의 세션 및 로그인 인프라를 100% 무중단 유지.
- **VirtualBox Polling Observer Bypass**
  - VirtualBox 공유 폴더 특성상의 `inotify` 이벤트 차단 한계를 극복하기 위해 `watchdog` 엔진을 100ms 정밀 폴링 상태로 커스텀 튜닝.
- **Foreground Infinite Monitor Lock**
  - 터미널 포그라운드를 완벽하게 장악하여 불필요한 명령어 입력 취약점 침투 경로를 사전에 차단하는 보안 대시보드 시스템.

---

## 🏗️ Architecture Design

```text
[ External Attacker ] 
       │ (iptables Hashlimit / Drop Protection)
       ▼
 ┌───────────┐ Keepalive 64  ┌────────────────────────┐
 │   Nginx   │ ────────────> │ zero_container_1 (8080)│ ──┐
 │  Reverse  │               ├────────────────────────┤   │ 
 │   Proxy   │               │ zero_container_2 (8080)│   ├──> [ Redis Session Broker ]
 └───────────┘               ├────────────────────────┤   │    (Session Data Is Safe!)
                             │ zero_container_3 (8080)│ ──┘
                             └────────────────────────┘
                                         ▲
  ┌──────────────────────────────────────┘ (Shadow Kill & Auto Restarter)
  │
┌──────────────────────────────┐
│  zero_fortress_master_v2.py  │ <── [ PollingObserver (100ms) Watchdog ]
└──────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Linux Environment (Ubuntu / CentOS 권장)
- Docker & Docker-compose
- Python 3.x & `watchdog` 라이브러리 (`pip install watchdog`)

### 2. Deployment
본 아키텍처는 제어기 실행 한 번으로 커널 최적화, 네트워크 브릿지 생성, 분산 프록시 풀 빌드를 논스톱으로 처리합니다.

```bash
# 1. 저장소 복사
git clone https://github.com
cd hyper-zero-architecture

# 2. 실행 권한 부여 및 마스터 클러스터 가동
chmod +x run_all_defense.sh
sudo ./run_all_defense.sh
```

### 3. Log Compliance
모든 탐지 증적과 침입 추적 데이터는 **정보통신망 이용촉진 및 정보보호 등에 관한 법률 제46조(정보통신망의 안정성 확보 등)** 기준을 준수하여 물리 로그 장부에 즉시 영구 기록됩니다.
```bash
tail -f /var/log/secure_forensic.log
```

---

## 📜 License
This project is open-source tested under the MIT License.
