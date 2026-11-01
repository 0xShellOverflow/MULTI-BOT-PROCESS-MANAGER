# MULTI-BOT-PROCESS-MANAGER

A Windows launcher that runs multiple Python and Node.js scripts in separate console windows and restarts them automatically on crash.

ตัวเปิดสคริปต์ Python และ Node.js หลายไฟล์พร้อมกันบน Windows โดยแยกหน้าต่าง console และ restart อัตโนมัติเมื่อ crash

## 🌐 Language / ภาษา

- [English](#english)
- [ภาษาไทย](#ภาษาไทย)

---

# English

## Overview
`main.py` starts every script listed in `BOT_FILES` in its own console window, monitors each one in a dedicated thread, and restarts it when it exits with a non-zero code.

## Features
- Runs `.py` (via the current Python interpreter, unbuffered) and `.js` (via `node`) files
- One console window per script, titled `<folder> - <file>`
- Auto-restart on non-zero exit: up to 3 restarts, 5 s delay
- Ctrl+C terminates all child processes (`taskkill /F /T`)
- Rainbow ASCII banner (`pystyle`)

## Technologies Used
| Technology | Purpose |
|---|---|
| Python 3 | Main launcher |
| `pystyle` | Colored banner |
| `subprocess` / `threading` / `signal` | Process spawning, per-script monitoring, Ctrl+C handling |
| Node.js | Runs `.js` scripts |

## Requirements
- Windows (uses `cmd`, `taskkill`, `CREATE_NEW_CONSOLE`)
- Python 3 (f-strings are used, so 3.6+)
- `pystyle`
- Node.js in `PATH` (only if running `.js` files)

## Installation
```bash
git clone https://github.com/0xShellOverflow/REPOSITORY-NAME.git   # URL template, not verified
cd REPOSITORY-NAME
pip install pystyle
```

## Configuration
Edit `BOT_FILES` in `main.py` with your own absolute paths:
```python
BOT_FILES = [
    r"C:\path\to\your\script.py",
    r"C:\path\to\your\app\index.js",
]
MAX_RESTARTS, RESTART_DELAY = 3, 5
```
Supported extensions: `.py`, `.js`. Never commit tokens or secrets used by your scripts.

## Usage
```bash
python main.py
```
Press `Ctrl+C` to stop all managed processes.

## How It Works
1. Show banner and register the `SIGINT` handler.
2. Start one monitor thread per entry in `BOT_FILES`.
3. Validate the file and extension, then open it in a new console with its own folder as working directory.
4. Wait for exit. Exit code `0` stops monitoring. Otherwise restart after 5 s, up to 3 times.
5. On Ctrl+C, kill all running process trees.

## Project Structure
```text
.
└── main.py   # Launcher and process monitor
```

## Important Notes
- Windows only.
- Paths in `BOT_FILES` are hardcoded and must be changed before use.
- Missing files or unsupported extensions are skipped with an error message and not retried.
- The restart counter is never reset.
- Unquoted window titles containing special `cmd` characters (e.g. `&`) may break the command (untested).

## Author
**0xShellOverflow Group**

GitHub: https://github.com/0xShellOverflow

---

# ภาษาไทย

## เกี่ยวกับโปรเจกต์
`main.py` เปิดทุกไฟล์ใน `BOT_FILES` ในหน้าต่าง console แยกกัน เฝ้าดูแต่ละไฟล์ด้วย thread เฉพาะ และ restart เมื่อ process จบด้วย exit code ที่ไม่ใช่ 0

## ความสามารถหลัก
- รันไฟล์ `.py` (ผ่าน Python ตัวเดียวกับที่รัน launcher แบบ unbuffered) และ `.js` (ผ่าน `node`)
- แยก console ต่อสคริปต์ ตั้งชื่อหน้าต่างเป็น `<โฟลเดอร์> - <ไฟล์>`
- Restart อัตโนมัติเมื่อ crash สูงสุด 3 ครั้ง หน่วง 5 วินาที
- กด Ctrl+C เพื่อปิด process ลูกทั้งหมด (`taskkill /F /T`)
- แสดงโลโก้ ASCII สีรุ้งด้วย `pystyle`

## เทคโนโลยีที่ใช้พัฒนา
| เทคโนโลยี | หน้าที่ |
|---|---|
| Python 3 | ตัว launcher หลัก |
| `pystyle` | แสดงโลโก้สี |
| `subprocess` / `threading` / `signal` | เปิด process, เฝ้าดูแต่ละสคริปต์, จัดการ Ctrl+C |
| Node.js | รันสคริปต์ `.js` |

## ความต้องการของระบบ
- Windows (ใช้ `cmd`, `taskkill`, `CREATE_NEW_CONSOLE`)
- Python 3 (ใช้ f-string จึงต้อง 3.6 ขึ้นไป)
- `pystyle`
- Node.js ใน `PATH` (เฉพาะเมื่อรันไฟล์ `.js`)

## วิธีติดตั้ง
```bash
git clone https://github.com/0xShellOverflow/REPOSITORY-NAME.git   # เป็น URL template ยังไม่ได้ตรวจสอบ
cd REPOSITORY-NAME
pip install pystyle
```

## การตั้งค่า
แก้ `BOT_FILES` ใน `main.py` ให้เป็น path เต็มของคุณ
```python
BOT_FILES = [
    r"C:\path\to\your\script.py",
    r"C:\path\to\your\app\index.js",
]
MAX_RESTARTS, RESTART_DELAY = 3, 5
```
รองรับนามสกุล `.py`, `.js` ห้าม commit token หรือความลับของสคริปต์ที่นำมารัน

## วิธีใช้งาน
```bash
python main.py
```
กด `Ctrl+C` เพื่อหยุดทุก process

## หลักการทำงาน
1. แสดงโลโก้และตั้ง handler ให้ `SIGINT`
2. สร้าง thread เฝ้าดู 1 ตัวต่อ 1 ไฟล์ใน `BOT_FILES`
3. ตรวจไฟล์และนามสกุล แล้วเปิดใน console ใหม่โดยใช้โฟลเดอร์ของไฟล์เป็น working directory
4. รอจนจบ ถ้า exit code เป็น `0` จะหยุดเฝ้าดู ถ้าไม่ใช่จะ restart หลัง 5 วินาที สูงสุด 3 ครั้ง
5. เมื่อกด Ctrl+C จะฆ่า process ทั้งต้นไม้

## โครงสร้างโปรเจกต์
```text
.
└── main.py   # Launcher และตัวเฝ้าดู process
```

## หมายเหตุสำคัญ
- ใช้ได้เฉพาะ Windows
- Path ใน `BOT_FILES` ถูกฮาร์ดโค้ด ต้องแก้ก่อนใช้งาน
- ไฟล์ที่ไม่พบหรือนามสกุลไม่รองรับจะถูกข้ามพร้อมข้อความ error และไม่ retry
- ตัวนับ restart ไม่เคย reset
- ชื่อหน้าต่างที่มีอักขระพิเศษของ `cmd` (เช่น `&`) อาจทำให้คำสั่งพัง (ยังไม่ได้ทดสอบ)

## ผู้พัฒนา
**0xShellOverflow Group**

GitHub: https://github.com/0xShellOverflow
