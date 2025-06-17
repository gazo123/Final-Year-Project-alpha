#  Distributed Authentication Protocol for Global Mobility Networks

This project implements a privacy-preserving and fault-tolerant authentication scheme designed for Global Mobility Networks (GMNs). It eliminates the reliance on a centralized Home Server by using **Shamir’s Secret Sharing** to distribute authentication data across multiple Foreign Servers (FSs). The system is modeled to reflect realistic 5G cluster-based architecture, enabling scalable, edge-level authentication for roaming users.

---

## Project Overview

### Problem
Traditional authentication relies heavily on a central server (Home Server), leading to:
- High latency due to cross-network communication.
- Scalability issues with increased users.
- Privacy concerns and single points of failure.

### Solution
This project:
- Uses a **(t, n)** threshold scheme to split a user's secret key.
- Distributes the shares across multiple FS nodes.
- Allows authentication locally by reconstructing the key from *t* FSs.
- Avoids direct involvement of the Home Server during login, ensuring faster and decentralized authentication.

---

## 📁 Folder Structure

FINAL-YEAR-PROJECT/
├── Home Server/
│   ├── share_generator.py
│   |── main.py
│   ├── user_registry.py
│   └── share_distributor.py
│   └── config.py
│
├── Foreign Server/
│   ├── foreign_server.py
│   ├── config.py
│   ├── main.py
│   └── user_registry.py
│
├── Mobile User/
│   ├── mobile_user.py
│   ├── main.py
│   └── config.py
│
├── tester/         (contains scripts to check latency by changing threshold values)
│
├── README.md
└── .gitattributes



## 🛠 How to Run the Project

### **Step 1: Start Foreign Servers**

On **each Foreign Server device**, run the `main.py` script from the `Foreign Server/` directory:

```bash
python main.py
````

This will:

* Start a listener on each foreign server.
* Wait for incoming share distributions from the Home Server.

---

### **Step 2: Register Users and Distribute Shares (Home Server)**

On the **Home Server device**, run the `main.py` script from the `Home Server/` directory:

```bash
python main.py
```

This will:

* Prompt you to enter multiple users (username and secret key).
* Generate `(n, t)` secret shares for each user using Shamir's Secret Sharing.
* Distribute those shares securely to the active foreign servers.

---

### **Step 3: Authenticate User (Mobile User Device)**

On the **Mobile User device**, run the `main.py` script from the `Mobile User/` directory:

```bash
python main.py
```

This will:

* Ask you to enter a username and corresponding key.
* Let you choose which Foreign Server you want to authenticate with.
* Generate a `PID` (a hash of the username and key) and send it along with the username to the selected Foreign Server.

---

## 🔐 How Authentication Works (Behind the Scenes)

1. The **Mobile User** sends the `username` and `PID` (hash of username + key) to a chosen **Foreign Server**.
2. The Foreign Server sends a `get_share()` request to **t−1 other Foreign Servers**.
3. It collects `t` total shares (including its own) to **reconstruct the original secret key**.
4. The server computes a new `PID′` by hashing the reconstructed key and username.
5. If `PID′ == PID`, authentication is **successful**. Otherwise, it's **rejected**.

---

## ✅ Requirements

* Python 3.10+
* Modules used: `hashlib`, `socket`, `json`, etc. (ensure all dependencies are met)

---

## 👨‍💻 Author

* Pushan Karmakar
* Dibya Shankar Jha
* Arkapriya Chanda
* Pritam Chakroborty


