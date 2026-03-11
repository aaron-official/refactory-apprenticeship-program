```text
  ____   _ __   __ __  __ _____ _   _ _____ ____      _    ____ ___ 
 |  _ \ / \\ \ / /|  \/  | ____| \ | |_   _/ ___|    / \  |  _ \_ _|
 | |_) / _ \\ V / | |\/| |  _| |  \| | | | \___ \   / _ \ | |_) | | 
 |  __/ ___ \| |  | |  | | |___| |\  | | |  ___) | / ___ \|  __/| | 
 |_| /_/   \_\_|  |_|  |_|_____|_| \_| |_| |____/ /_/   \_\_|  |___|
```

# Payments API — TDD Training Assignment

This repository contains a complete, **test-first** implementation of a fake payment server, fulfilling the cumulative assignment for **Days 1–7** of the TDD Training Course. It simulates a REST API for charging cards, refunding transactions, and managing customer accounts entirely **in memory**.

The core focus of this project is not the infrastructure, but demonstrating a rigorous **TDD Cycle (Red → Green → Refactor)**, effective test coverage, and modular application design using test doubles (Fakes, Stubs, and Spies).

---

## 🚀 Tech Stack

- **FastAPI** — High-performance HTTP routing and web layer
- **pytest & httpx** — Test runner, assertions, and async HTTP client for integration testing
- **uv** — Lightning-fast Python package and environment manager
- **Scalar** — Modern API documentation UI available at `/docs` or the stylized root `/` page.

---

## 🛠️ Setup & Running

1. **Install uv** (if you don't have it):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or on Windows PowerShell:
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Sync Dependencies**:
   ```bash
   uv sync
   ```

3. **Run the API Server**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

   - Navigate to `http://localhost:8000/` for the stylized ASCII landing page.
   - Navigate to `http://localhost:8000/docs` to view the comprehensive API endpoints in Scalar.

---

## 🧪 Testing Approach & Tasks

This project strictly followed the rule: **Write a failing test before writing any implementation code.**

Run the entire suite of **90 tests** with:
```bash
uv run pytest
```

### 1. Unit Tests (`tests/unit/`)
*Corresponding Task: Task 1 (Validators)*
Contains pure logic tests verifying primitive boundaries, edge cases, and value generators.
- `test_validators.py` covers amount types (rejecting decimals/negatives/nulls), string lengths, and email logic.
```bash
uv run pytest tests/unit/
```

### 2. Service Layer Tests (`tests/services/`)
*Corresponding Task: Task 2 (TDD Cycle for PaymentService)*
Focuses on the core business logic. 
- `test_payment_service.py` is the application's "brain", taking the requirements (creating customers, charging payments, checking boundaries on refunds) and driving the development through strict Red → Green → Refactor cycles independent of the database or HTTP layer.
```bash
uv run pytest tests/services/
```

### 3. Repository & Doubles Tests (`tests/repos/`)
*Corresponding Task: Task 3 (Fake Repository)*
- `test_fake_payment_repo.py` handles our in-memory data store tests.
- **Fakes**: A full `FakePaymentRepo` simulating database states, reads, and writes.
- **Stubs**: Simulating specific scenario returns (e.g., forcing a payment status to test service state changes).
- **Spies**: Verifying that side-effects like `logger.warning` are triggered exactly when a transaction gracefully fails.
```bash
uv run pytest tests/repos/
```

### 4. Web Layer / Route Tests (`tests/routes/`)
*Corresponding Task: Task 4 & 5 (Web TDD and Edge Cases)*
Tests the endpoints (`/customers`, `/payments`, `/refunds`) via FastAPI's `TestClient` (backed by `httpx`).
- Validates 200/201 Success codes.
- Asserts strict 400 Validation failures when bodies have missing keys (Task 5).
- Ensures 404 Not Found returns correctly for unknown resource IDs.
- Validates internal 500 exceptions fall back safely without exposing stack traces.
```bash
uv run pytest tests/routes/
```

---

## 📂 Project Structure

The codebase groups domains strictly by layer, separating configuration, route delivery, business services, and storage:

```
payments_api/
│
├── app/
│   ├── main.py                  # FastAPI instantiation, startup events, and global exception handlers
│   ├── routes/                  # HTTP Endpoints (Task 4 & 5)
│   │   ├── customers.py
│   │   ├── payments.py
│   │   └── refunds.py
│   ├── services/                # Core Business Logic (Task 2)
│   │   └── payment_service.py
│   ├── repos/                   # In-Memory Storage & Querying (Task 3)
│   │   └── fake_payment_repo.py
│   └── utils/                   # Pure Functions & Data Checks (Task 1)
│       └── validators.py
│
├── tests/                       # Mirrored structure isolating test concerns
│   ├── unit/                    # Task 1
│   ├── services/                # Task 2
│   ├── repos/                   # Task 3
│   └── routes/                  # Task 4 & 5
│
├── pyproject.toml               # Modern standard packaging, uv config, and pytest paths
└── README.md
```

---

## 💡 Course Reflections

Implementing this via the TDD cycle heavily influenced the separation of concerns. The `PaymentService` tests immediately exposed the need for dependency injection (passing `FakePaymentRepo` into the service block rather than instantiating it internally). 

Furthermore, doing Web API testing immediately highlighted how HTTP logic (extracting JSON, returning 201s vs 400s) clutters business logic, forcing a clean divide between the endpoints in `app/routes/` and the underlying logic in `app/services/`. Writing boundary tests around the refund logic prevented a common bug of accidentally allowing a customer to be refunded past their total payment amount across multiple separate partial refunds.
