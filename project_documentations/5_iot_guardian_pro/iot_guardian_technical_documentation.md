# IoT Guardian Pro — Technical Documentation
*Interactive Security Breach Simulator & Network Analytics Dashboard*

This document provides a comprehensive technical overview of the **IoT Guardian Pro** simulation system located at `E:/PROJECTS/INTERN/PROJECT_ONE/breach-simu`.

---

## 1. Executive Summary
**IoT Guardian Pro** is an educational cyber-range and security simulator. It runs automated, harmless attack simulations (DDoS spikes, Dictionary Brute-Force, and Phishing) to teach administrators how anomalies look on network charts. It supports live telemetry via WebSockets and exports PDF/Excel incident reports.

---

## 2. Platform Architecture

The project has four distinct components:
1. **FastAPI Backend (`backend/`)**: Handles database entries, logs match history, manages SQLite states, and executes WebSocket network simulations.
2. **React Dashboard (`frontend/`)**: Displays real-time packet speeds, attack vectors, system stats, and generates audit reports.
3. **Landing Page (`landing-page/`)**: Introducing corporate portal services.
4. **Phishing Target (`phishing-site/`)**: A mock login screen (`login.html`) to demonstrate phishing vector captures.

```
                  ┌──────────────────────┐
                  │    React Dashboard   │
                  └──────────┬───────────┘
                             │ HTTP / WebSockets
                             ▼
                  ┌──────────────────────┐
                  │    FastAPI Backend   │
                  └──────┬────────┬──────┘
                         │        │
            ┌────────────┘        └────────────┐
            ▼                                  ▼
   ┌──────────────────┐               ┌──────────────────┐
   │ SQLite Database  │               │ Simulations      │
   │ - Audit Logs     │               │ - DDoS Floods    │
   │ - User Records   │               │ - Brute Force    │
   └──────────────────┘               │ - Phishing Site  │
                                      └──────────────────┘
```

---

## 3. Core Simulation Modules

### A. DDoS Simulation
Simulates packet spikes. When activated:
* The backend increases simulated packets/second rates by 500%.
* Sends high-speed streams via `/ws` to the frontend.
* Charts display latency spikes and packet rate peaks.

### B. Brute-Force Simulation
Runs a mock login dictionary attack:
* Ingests passwords from a trimmed `rockyou.txt` dictionary file.
* Simulates hundreds of invalid login attempts against the system.
* Triggers alert notifications once threshold rates are breached.

### C. Phishing Simulation
* Hosts a mock authentication page.
* Records username/password credentials entered during simulation runs (safely logged inside SQLite).
* Teaches users about credentials harvesting vectors.

---

## 4. Reports Generation (PDF & Excel)

The dashboard allows exporting audit sheets:
* **PDF Audits**: Uses `reportlab` to design dynamic PDFs detailing incident timelines, attack categories, IP origins, and severity.
* **Excel Reports**: Uses `openpyxl` to write data rows of all simulated logs, allowing easy parsing by analyst teams.

---

## 5. Setup & Execution Instructions

### Setup Backend
1. Go to backend:
   ```bash
   cd E:/PROJECTS/INTERN/PROJECT_ONE/breach-simu/backend
   ```
2. Install libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run FastAPI:
   ```bash
   uvicorn app.main:app --reload
   ```

### Setup Frontend
1. Go to frontend:
   ```bash
   cd E:/PROJECTS/INTERN/PROJECT_ONE/breach-simu/frontend
   ```
2. Install and launch:
   ```bash
   npm install
   npm run dev
   ```
