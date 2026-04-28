# Alibaba Bailian API Concurrent Test

เครื่องมือทดสอบ concurrent สำหรับ Alibaba Bailian (Coding Plan) API

## Features

- ทดสอบ concurrent requests ไปยัง Bailian API
- รองรับทั้ง OpenAI-compatible และ Anthropic-compatible protocol
- รองรับทุกโมเดลที่มี: Qwen, Zhipu (GLM), Kimi, MiniMax
- อ่าน API key จาก `KEY_SOURCE` ใน `.env` โดยอัตโนมัติ — ไม่มีเก็บในโปรเจกต์

## Setup

```bash
cd ~/projects/api_concurrent_test
uv sync
```

## Usage

### รันเทสด้วยค่าเริ่มต้น

```bash
uv run python concurrent_test.py
```

### เปลี่ยนโมเดล

แก้ `TEST_MODEL` ใน `config.py`:

```python
TEST_MODEL = "glm-5"  # หรือ qwen3.6-plus, kimi-k2.5, MiniMax-M2.5, ฯลฯ
```

### เปลี่ยนจำนวน concurrent / จำนวนครั้ง

```python
CONCURRENCY_LEVEL = 20   # จำนวน request พร้อมกัน
TOTAL_REQUESTS = 200     # จำนวน request ทั้งหมด
```

### สลับไปใช้ Anthropic protocol

แก้ `API_URL` ใน `config.py`:

```python
API_URL = f"{ANTHROPIC_COMPATIBLE_BASE_URL}/messages"
# Default: f"{OPENAI_COMPATIBLE_BASE_URL}/chat/completions"
```

### เปลี่ยน prompt

```python
DEFAULT_PAYLOAD = {
    "model": TEST_MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain concurrency in 1 sentence"}
    ]
}
```

## Available Models

| Brand   | Model                  | Capabilities                              |
|---------|------------------------|-------------------------------------------|
| Qwen    | qwen3.6-plus           | Text Generation, Deep Thinking, Visual    |
| Qwen    | qwen3.5-plus           | Text Generation, Deep Thinking, Visual    |
| Qwen    | qwen3-max-2026-01-23   | Text Generation, Deep Thinking            |
| Qwen    | qwen3-coder-next       | Text Generation                           |
| Qwen    | qwen3-coder-plus       | Text Generation                           |
| Zhipu   | glm-5                  | Text Generation, Deep Thinking            |
| Zhipu   | glm-4.7                | Text Generation, Deep Thinking            |
| Kimi    | kimi-k2.5              | Text Generation, Deep Thinking, Visual    |
| MiniMax | MiniMax-M2.5           | Text Generation, Deep Thinking            |

## Configuration

ค่าทั้งหมดอยู่ใน `config.py`:

| Setting                    | Default                                   | Description                |
|----------------------------|-------------------------------------------|----------------------------|
| `OPENAI_COMPATIBLE_BASE_URL` | `https://coding-intl.dashscope.aliyuncs.com/v1` | OpenAI protocol endpoint   |
| `ANTHROPIC_COMPATIBLE_BASE_URL` | `https://coding-intl.dashscope.aliyuncs.com/apps/anthropic` | Anthropic protocol endpoint |
| `API_URL`                  | `{OPENAI_BASE}/chat/completions`          | Endpoint ที่ใช้จริง        |
| `TEST_MODEL`               | `qwen3.6-plus`                            | โมเดลสำหรับเทส             |
| `CONCURRENCY_LEVEL`        | `10`                                      | จำนวน request พร้อมกัน     |
| `TOTAL_REQUESTS`           | `100`                                     | จำนวน request ทั้งหมด      |
| `TIMEOUT_SECONDS`          | `30`                                      | Timeout ต่อครั้ง            |

## Output

หลังรันจะแสดง:
- จำนวนสำเร็จ / ล้มเหลว
- เวลาทั้งหมด
- Avg / Min / Max response time
- Requests per second
- รายการ error (ถ้ามี)

### ทำความเข้าใจตัวเลขหลัก

| ตัวชี้วัด | ความหมาย | ตัวอย่าง |
|-----------|----------|----------|
| `Requests/sec` | ความเร็ว **เฉลี่ย** ทั้งเทส (100 req ÷ เวลาทั้งหมด) | `21.25` = เฉลี่ย 21 คำขอ/วินาที |
| `Peak requests/sec` | ความเร็วสูงสุดใน 1 วินาทีใด 1 วินาที (จุดที่คึกคักที่สุด) | `71` = วินาทีที่เร็วสุดมี 71 คำขอเสร็จ |

**ทำไมตัวเลขต่างกันเยอะ?**
- `Requests/sec` ดึงลงเพราะช่วงท้ายมี 429 (rate limit) คำขอช้าลง
- `Peak requests/sec` จับเฉพาะวินาทีที่เร็วที่สุด — บ่งบอกว่า API รับได้สูงสุดประมาณนี้

**ใช้ยังไง:**
- ดู `Peak` เพื่อรู้ **ขีดจำกัดสูงสุด** ของ API
- ดู `Requests/sec` เพื่อรู้ **ความเร็วจริง** ที่ใช้งานได้อย่างต่อเนื่อง

## API Key

**โปรเจกต์นี้ไม่มีเก็บ API key ไว้ในโค้ดหรือ `.env` ของตัวเองเลย**

### ไฟล์ที่อ่าน

```
~/projects/your-project/.env
```

อ่านค่าจากบรรทัดที่ขึ้นต้นด้วย `BAILIAN_API_KEY` เช่น:

```env
BAILIAN_API_KEY=sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### ทำไมอ่านจากโปรเจกต์อื่น?

เพื่อป้องกันไม่ให้ credential หลุดขึ้น Git โดยไม่ได้ตั้งใจ — ไฟล์ `.env` ของโปรเจกต์อื่นถูก `.gitignore` อยู่แล้ว และโปรเจกต์นี้ยังอ่านจากแหล่งกลางแหล่งเดียว ไม่ต้องคัดลอกหรือเก็บซ้ำ

### ต้องเตรียมอะไรก่อนรัน

1. ตั้งค่า `KEY_SOURCE` ใน `.env` ของโปรเจกต์นี้ ให้ชี้ไปยังไฟล์ `.env` ที่มี `BAILIAN_API_KEY`
2. ตรวจสอบว่าไฟล์เป้าหมายมี `BAILIAN_API_KEY`
3. ไม่ต้องสร้าง `.env` แยกในโปรเจกต์นี้

## วิธีการทำงานของโค้ดทดสอบ

### ใช้ `asyncio` (Asynchronous)

โปรเจกต์นี้ใช้ **asynchronous I/O** ไม่ใช่ synchronous — ทุกคำขอทำงานพร้อมกันแบบไม่บล็อกกัน

### โครงสร้างหลัก

```
asyncio.run()
  └── run_concurrent_test()
        ├── สร้าง ClientSession (HTTP connection pool)
        ├── สร้าง Semaphore จำกัดจำนวนคำขอพร้อมกัน
        ├── สร้าง Task 100 ตัว (ตาม TOTAL_REQUESTS)
        └── asyncio.gather(*tasks) — รอทุกคำขอเสร็จพร้อมกัน
              └── Semaphore ปล่อยทีละ N คำขอ (ตาม CONCURRENCY_LEVEL)
```

### ทำไมใช้ asyncio?

| Synchronous              | Asynchronous (asyncio)        |
|--------------------------|-------------------------------|
| รันทีละ 1 คำขอ             | รัน 10-100 คำขอพร้อมกัน        |
| ถ้า API ตอบช้า = รอนาน     | ไม่ต้องรอ — ส่งคำขออื่นทับได้ |
| 100 คำขอ ใช้เวลาหลายนาที   | 100 คำขอ ใช้เวลาไม่กี่วินาที   |

### กลไกสำคัญ

1. **`ClientSession` (aiohttp)** — สร้าง HTTP connection pool เดียว ใช้ร่วมกันทุกคำขอ ไม่ต้องเปิด-ปิดทีละครั้ง
2. **`Semaphore`** — ควบคุมให้ส่งคำขอพร้อมกันได้สูงสุด `CONCURRENCY_LEVEL` คำขอ ถ้าเกินจะรอจนกว่ามีช่องว่าง
3. **`asyncio.gather()`** — รันทุกคำขอพร้อมกันและรอจนกว่าทุกตัวเสร็จ

### ลำดับการทำงาน

```
เริ่ม ──► สร้าง Semaphore(10) ──► สร้าง 100 Tasks
                                     │
                                     ├─ Task 0-9  เริ่มพร้อมกัน (10 ตัวแรก)
                                     ├─ เมื่อตัวใดเสร็จ ──► Task 10 เข้าแทน
                                     ├─ ... จนครบ 100 ตัว
                                     │
                                     └─ ทุกคำขอเสร็จ ──► รวมผล
                                          ├── สำเร็จ / ล้มเหลว
                                          ├── Avg / Min / Max response time
                                          └── Requests / second
```
