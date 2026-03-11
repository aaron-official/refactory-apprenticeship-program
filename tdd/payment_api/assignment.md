# TDD Training Course · Weeks 1 & 2  
## Days 1–7 | Cumulative Assignment

# Payments API

Build a complete, **tested fake payment server from scratch — test-first**.

**Topics Covered**

- Unit Testing
- TDD Cycle
- Refactoring
- Mocks, Stubs, Fakes & Spies
- Web TDD
- Edge Cases & Error Handling

---

## Stack

Choose **one**:

- **Express + Jest**
- **FastAPI + pytest**

---

## Deliverable

- GitHub repository
- Working API
- Full test suite
- README

---

## Estimated Time

**5–7 hours**

---

## Due

Before the **Day 8 session** — submit your GitHub link via the course portal.

---

# 1. What You're Building

You will build a **fake Payment Server** — a REST API that simulates:

- Charging cards
- Refunding transactions
- Managing customer accounts

It does **not connect to a real payment provider**.  
All data lives **in memory**.

The **goal is the test suite**, not the infrastructure.

This is a **cumulative assignment covering all seven days** of the course.  
Each task maps to specific sessions and requires the techniques taught there.

---

## Course Techniques Mapping

| Day | Technique | Where it Appears |
|----|----|----|
| 1 | Intro to TDD – Red / Green / Refactor mindset | Every task — test first |
| 2 | Unit Testing – Frameworks, matchers, structure | Task 1 — unit tests |
| 3 | Full TDD Cycle | Task 2 — PaymentService |
| 4 | Refactoring & Code Smells | Task 2 — refactor after green |
| 5 | Mocks, Stubs, Fakes, Spies | Task 3 — FakeRepo + mocks |
| 6 | Web TDD | Task 4 — HTTP route tests |
| 7 | Edge Cases & Error Handling | Task 5 — invalid inputs |

---

## The One Rule That Cannot Be Broken

**Write the failing test before you write any implementation code.**

Every single time.

If your **commit history does not show tests before features**, that is an **automatic deduction**.

---

# 2. The Domain — Fake Payment Server

This is a **sandbox payment API**.

It supports:

- Creating customers
- Charging a card
- Refunding payments
- Listing transactions

The system does **not connect to any real payment gateway**.

All data lives **in memory using a fake repository**.

---

# Core Entities

## Customer

```
Customer
id: string
email: string
balance: number
```

---

## Payment

```
Payment
id: string
customerId: string
amount: number
status: "succeeded" | "refunded"
createdAt: timestamp
```

---

# 3. API Endpoints

## Create Customer

```
POST /customers
```

Request

```json
{
  "email": "user@email.com"
}
```

Response

```json
{
  "id": "cust_123",
  "email": "user@email.com",
  "balance": 0
}
```

---

## Charge Customer

```
POST /payments
```

Request

```json
{
  "customerId": "cust_123",
  "amount": 500
}
```

Response

```json
{
  "id": "pay_456",
  "customerId": "cust_123",
  "amount": 500,
  "status": "succeeded"
}
```

---

## Refund Payment

```
POST /refunds
```

Request

```json
{
  "paymentId": "pay_456"
}
```

Response

```json
{
  "status": "refunded"
}
```

---

## List Customer Payments

```
GET /customers/{customerId}/payments
```

Response

```json
[
  {
    "id": "pay_456",
    "amount": 500,
    "status": "succeeded"
  }
]
```

---

# 4. Task Breakdown

## Task 1 — Unit Tests First

Write unit tests for:

- Payment amount validation
- Customer existence
- Refund logic

Tests should cover:

- Valid charge
- Negative amounts
- Missing customer
- Double refund

---

## Task 2 — PaymentService (TDD Cycle)

Implement `PaymentService` **using the TDD cycle**.

Steps:

1. Write failing test
2. Implement minimal code
3. Refactor safely

Responsibilities:

- Charge customer
- Store payment
- Handle refund logic

---

## Task 3 — Fake Repository

Create an **in-memory repository**.

Example:

```
FakePaymentRepo
FakeCustomerRepo
```

Use this to simulate:

- Database reads
- Database writes

Tests should verify:

- Repository calls
- Stored values
- Edge cases

---

## Task 4 — Web Layer TDD

Build the **HTTP API routes**.

Test them with:

### Express

```
supertest
```

### FastAPI

```
TestClient
```

Every endpoint must have:

- Success test
- Validation failure test
- Not-found test

---

## Task 5 — Edge Cases

Handle the following:

- Negative payment amounts
- Non-existent customer
- Double refunds
- Invalid IDs
- Internal service failures

Return proper HTTP codes:

| Case | Code |
|----|----|
| Success | 200 |
| Invalid request | 400 |
| Not found | 404 |
| Server error | 500 |

---

# 5. Project Structure

Example (Node):

```
payments-api
│
├── src
│   ├── services
│   │   └── PaymentService.js
│   ├── repositories
│   │   └── FakePaymentRepo.js
│   ├── routes
│   │   └── payments.js
│   └── app.js
│
├── tests
│   ├── unit
│   └── integration
│
├── package.json
└── README.md
```

Example (Python):

```
payments_api
│
├── app
│   ├── services
│   ├── repositories
│   ├── routes
│   └── main.py
│
├── tests
│
└── README.md
```

---

# 6. Evaluation Criteria

| Area | Weight |
|----|----|
| Test Coverage | High |
| TDD Discipline | High |
| Code Quality | Medium |
| API Correctness | Medium |
| Edge Cases | Medium |

---

# 7. Submission

Submit:

- GitHub repository link
- README with setup instructions
- All tests passing

Before the **Day 8 session**.

---

# Final Reminder

**Always follow the TDD cycle**

```
RED → GREEN → REFACTOR
```

Write the **test first**, then implement the code.