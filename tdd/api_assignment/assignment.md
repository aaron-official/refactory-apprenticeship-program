# TDD Training Course · Weeks 1 & 2
## Days 1–7 | Cumulative Assignment

# Payments API

> Build a complete, tested fake payment server from scratch — test-first.

**Topics:** Unit Testing · TDD Cycle · Refactoring · Mocks, Stubs, Fakes & Spies · Web TDD · Edge Cases & Error Handling

| | |
|---|---|
| **Stack** | Express + Jest **OR** FastAPI + pytest (your choice) |
| **Deliverable** | GitHub repo — working API + full test suite + README |
| **Estimated Time** | 5–7 hours |
| **Due** | Before the Day 8 session — submit your GitHub link via the course portal |

---

## 1. What You're Building

You will build a **fake Payment Server** — a REST API that simulates charging cards, refunding transactions, and managing customer accounts. It does not connect to a real payment provider. The data lives in memory. The goal is the test suite, not the infrastructure.

This is a cumulative assignment covering all seven days of the course. Each task maps to specific sessions and requires the techniques taught there.

| Day | Topic | Technique | Where it appears in this assignment |
|-----|-------|-----------|--------------------------------------|
| 1 | Intro to TDD | Red–Green–Refactor mindset | Every task — test first, always |
| 2 | Unit Testing Fundamentals | Frameworks, matchers, test structure | Task 1 — unit tests for payment validation helpers |
| 3 | First Full TDD Cycle | Iterative RED → GREEN → REFACTOR | Task 2 — build PaymentService end-to-end TDD |
| 4 | Refactoring & Design via TDD | Code smells, safe refactoring | Task 2 — refactor with confidence after green |
| 5 | Working with Dependencies | Mocks, Stubs, Fakes, Spies | Task 3 — FakeRepo, stub, spy. Task 4 — mock service in routes |
| 6 | TDD for Web Apps | In-process HTTP testing | Task 4 — every route tested via supertest / TestClient |
| 7 | Edge Cases & Error Handling | Boundaries, 404s, 500s | Task 5 — invalid amounts, bad IDs, service failures |

> ⚠️ **The one rule that cannot be broken**
> Write the failing test before you write any implementation code. Every single time. If your commit history does not show test commits before feature commits, that is an automatic deduction.

---

## 2. The Domain — Fake Payment Server

This is a sandbox payment API — similar to Stripe's test mode. It accepts fake card details, processes imaginary charges, and records transactions. No money moves. No real card networks are contacted.

### 2.1 Resources

The API manages three resources.

| Resource | Shape | Key rules |
|----------|-------|-----------|
| Customer | `{ "id":"cus_1", "name":"Alice", "email":"alice@example.com" }` | `name` and `email` required. Email must be unique. Max name: 100 chars. |
| Payment | `{ "id":"pay_1", "customerId":"cus_1", "amount":2999, "currency":"usd", "status":"succeeded" }` | Amount in pence/cents (integer ≥ 1). Currency is a 3-char code. Status: `pending` → `succeeded` or `failed`. |
| Refund | `{ "id":"ref_1", "paymentId":"pay_1", "amount":2999, "status":"succeeded" }` | Cannot exceed the original payment amount. Only `succeeded` payments can be refunded. |

> 💡 **Why integers for amounts?**
> Real payment APIs (Stripe, Adyen, GoCardless) store amounts as integers in the smallest currency unit — pence, cents, etc. This avoids floating-point rounding errors. £29.99 is stored as `2999`. Your API must do the same: reject decimal amounts.

### 2.2 Architecture — Three Layers

| Layer | Example file | Does what | Test with |
|-------|-------------|-----------|-----------|
| Route | `routes/payments.js` | Handle HTTP. Validate input shape. Call service. Return status code + JSON. | Mock the service. Use supertest or TestClient. |
| Service | `services/paymentService.js` | Business rules: amount validation, status transitions, refund limits. | Inject FakeRepository. Pure unit tests. |
| Repository | `repos/paymentRepo.js` | Data access. Real version would hit a DB. In tests: swap in a Fake. | FakeRepository — in-memory Map / dict. |

---

## 3. API Specification

Build all endpoints below. The 'Day' column shows which session's technique to apply when writing that endpoint's tests.

| Method | Endpoint | Description | Returns | Day |
|--------|----------|-------------|---------|-----|
| POST | `/customers` | Create a new customer | 201 / 400 | D2/3 |
| GET | `/customers/:id` | Get one customer by ID | 200 / 404 | D7 |
| GET | `/customers/:id/payments` | List all payments for a customer | 200 / 404 | D7 |
| POST | `/payments` | Create a charge (status: pending) | 201 / 400 | D2/3 |
| GET | `/payments/:id` | Get one payment by ID | 200 / 404 | D7 |
| POST | `/payments/:id/capture` | Capture a pending payment → succeeded | 200 / 404 | D6 |
| POST | `/payments/:id/fail` | Fail a pending payment → failed | 200 / 404 | D6 |
| POST | `/refunds` | Create a refund against a payment | 201 / 400 | D5/6 |
| GET | `/refunds/:id` | Get one refund by ID | 200 / 404 | D7 |
| GET | `/payments` | List all payments (optional filter) | 200 | D6 |

### 3.1 Validation & Business Rules

These rules are enforced at the service layer and tested at both the service level and the route level.

**Customers**
- `name`: required, 1–100 characters, must not be whitespace-only
- `email`: required, must contain `@`, must be unique across all customers

**Payments**
- `customerId`: required, must reference an existing customer
- `amount`: required integer ≥ 1 (pence/cents). Reject decimals, zero, and negative values
- `currency`: required, must be exactly 3 characters (e.g. `usd`, `gbp`, `eur`)
- `status` starts as `pending`. Only pending payments can be captured or failed
- A failed or succeeded payment cannot be captured, failed, or refunded again

**Refunds**
- `paymentId`: required, must reference an existing payment
- The referenced payment must have status `succeeded` (cannot refund pending or failed)
- `amount`: required integer ≥ 1. Cannot exceed the original payment amount
- Partial refunds are allowed. Total refunds across all refunds must not exceed the original amount

---

## 4. Tasks

Complete the tasks in order. The FakeRepository from Task 3 is needed by Task 2 — skim the interface first, then return to implement it after Task 2 tests are written.

---

### Task 1 — Unit Testing Fundamentals

**Technique:** Matchers · Assertions · Test structure (Days 1, 2, 3)

Start with pure validation functions — no HTTP, no state, no dependencies. Get comfortable with the test framework and the right matchers before you build anything complex.

**What to build**
- `validateAmount(amount)` — returns `true` if amount is a positive integer, `false` otherwise
- `validateCurrency(currency)` — returns `true` if currency is a non-empty 3-character string
- `validateEmail(email)` — returns `true` if email contains `@` and `.`
- `generateId(prefix)` — returns a prefixed unique string e.g. `generateId('pay')` → `'pay_abc123'`

**Required tests — write these test-first**

1. `validateAmount` returns `true` for `100`
2. `validateAmount` returns `true` for `1` (minimum boundary)
3. `validateAmount` returns `false` for `0`
4. `validateAmount` returns `false` for `-1`
5. `validateAmount` returns `false` for `9.99` (decimal — not allowed)
6. `validateAmount` returns `false` for `null`
7. `validateAmount` returns `false` for a string like `'100'`
8. `validateCurrency` returns `true` for `'usd'`
9. `validateCurrency` returns `false` for `'us'` (too short)
10. `validateCurrency` returns `false` for `'usdd'` (too long)
11. `validateCurrency` returns `false` for an empty string
12. `validateEmail` returns `true` for `'alice@example.com'`
13. `validateEmail` returns `false` for a string with no `@`
14. `validateEmail` returns `false` for an empty string
15. `generateId` returns a string starting with the given prefix
16. `generateId` returns a different value on each call

> 💡 **Day 2 technique — use the right matcher**
> `toBe()` for primitives only. `toEqual()` for objects. `toBeNull()` for null. `toStrictEqual()` when checking object shape precisely. `toThrow()` / `pytest.raises()` for errors. Never use `toBe()` to compare two objects — it checks reference equality and will fail even when values match.

---

### Task 2 — Full TDD Cycle: PaymentService

**Technique:** RED → GREEN → REFACTOR (Days 1, 3, 4)

Build `PaymentService` using a full TDD cycle. Inject a `FakeRepository`. No real database. No HTTP. Just business logic and unit tests.

**PaymentService interface to implement**
```javascript
// JavaScript
class PaymentService {
  constructor(repo) { this.repo = repo; }
  async createCustomer(name, email) { ... }
  async createPayment(customerId, amount, currency) { ... } // status: 'pending'
  async capture(paymentId) { ... }   // pending → succeeded
  async fail(paymentId) { ... }      // pending → failed
  async refund(paymentId, amount) { ... }
  async getPayment(id) { ... }
  async getCustomer(id) { ... }
  async getPaymentsForCustomer(customerId) { ... }
}
```
```python
# Python
class PaymentService:
  def __init__(self, repo): self.repo = repo
  def create_customer(self, name, email): ...
  def create_payment(self, customer_id, amount, currency): ...
  def capture(self, payment_id): ...
  def fail(self, payment_id): ...
  def refund(self, payment_id, amount): ...
  def get_payment(self, id): ...
  def get_customer(self, id): ...
  def get_payments_for_customer(self, customer_id): ...
```

**Required service tests — 18 tests, all written before implementation**

1. `createCustomer()` returns a customer with the correct name and email
2. `createCustomer()` generates a unique id prefixed with `'cus_'`
3. `createCustomer()` throws `'Name is required'` when name is empty
4. `createCustomer()` throws `'Invalid email'` when email has no `@`
5. `createCustomer()` throws `'Email already exists'` when email is registered twice
6. `createPayment()` returns a payment with status `'pending'`
7. `createPayment()` generates a unique id prefixed with `'pay_'`
8. `createPayment()` throws `'Customer not found'` when customerId is unknown
9. `createPayment()` throws `'Invalid amount'` when amount is `0`
10. `createPayment()` throws `'Invalid amount'` when amount is negative
11. `createPayment()` throws `'Invalid amount'` when amount is a decimal like `9.99`
12. `createPayment()` throws `'Invalid currency'` when currency is not 3 characters
13. `capture()` changes payment status from `'pending'` to `'succeeded'`
14. `capture()` throws `'Payment not found'` when id is unknown
15. `capture()` throws `'Cannot capture'` when payment status is already `'succeeded'`
16. `capture()` throws `'Cannot capture'` when payment status is `'failed'`
17. `fail()` changes payment status from `'pending'` to `'failed'`
18. `refund()` throws `'Payment not found'` when paymentId is unknown

**Refund boundary tests (write at service level)**

19. `refund()` succeeds when refund amount equals exactly the payment amount (full refund)
20. `refund()` throws `'Refund exceeds payment amount'` when refund is greater than payment
21. `refund()` throws `'Cannot refund'` when payment status is `'pending'`
22. `refund()` throws `'Cannot refund'` when payment status is `'failed'`

**Refactoring requirement (Day 4)**

Once all tests are green, look for these code smells and fix them — without breaking any test:
- Duplicated validation logic across `createPayment` and `refund` — extract a `validateAmount()` private method
- Status transition logic repeated in `capture()` and `fail()` — extract a private `transitionStatus()` helper
- Magic strings like `'pending'`, `'succeeded'`, `'failed'` — extract as a `STATUS` constants object
- Long `createPayment()` doing too many things — split into smaller private steps

> 💡 **Day 4 technique — refactor with confidence**
> Rename methods, extract helpers, introduce constants — none of this should break a single test. If a test breaks during refactoring, you changed observable behaviour (not just structure), or the test was checking implementation details. Fix the code, not the test.

---

### Task 3 — FakeRepository & Test Doubles

**Technique:** Fakes · Stubs · Spies (Day 5)

Build the `FakeRepository` used by your service tests, then demonstrate stub and spy techniques with payment-specific examples.

**FakePaymentRepository — methods to implement**
- `saveCustomer(customer)` — stores by id, returns the saved customer
- `findCustomerById(id)` — returns customer or `null`
- `findCustomerByEmail(email)` — returns customer or `null` (for uniqueness check)
- `savePayment(payment)` — stores by id, returns the saved payment
- `findPaymentById(id)` — returns payment or `null`
- `findPaymentsByCustomer(customerId)` — returns array of matching payments
- `saveRefund(refund)` — stores by id, returns the saved refund
- `findRefundsByPayment(paymentId)` — returns all refunds for a payment (for over-refund check)
- `clear()` — removes all data. Call in `beforeEach`.

**Required tests — test the Fake itself (8 tests)**

1. `saveCustomer()` stores a customer so `findCustomerById()` returns it
2. `findCustomerById()` returns `null` for an unknown id
3. `findCustomerByEmail()` returns the customer when email matches
4. `findCustomerByEmail()` returns `null` when email does not match
5. `savePayment()` stores a payment so `findPaymentById()` returns it
6. `findPaymentsByCustomer()` returns only payments for the given `customerId`
7. `findRefundsByPayment()` returns all refunds linked to a payment
8. `clear()` empties all stored data

**Stub test — simulate a payment gateway response**

Write one test that stubs the repository to return a specific payment. This is how you test `capture()` logic without needing a Fake that actually stores data.
```javascript
// JavaScript — stub example
test('capture sets status to succeeded', async () => {
  const stubRepo = {
    findPaymentById: jest.fn().mockResolvedValue({
      id: 'pay_1', amount: 1000, status: 'pending'
    }),
    savePayment: jest.fn().mockImplementation(p => Promise.resolve(p))
  };
  const service = new PaymentService(stubRepo);
  const result = await service.capture('pay_1');
  expect(result.status).toBe('succeeded');
});
```
```python
# Python — stub example
def test_capture_sets_status_to_succeeded():
  stub_repo = MagicMock()
  stub_repo.find_payment_by_id.return_value = {
    'id': 'pay_1', 'amount': 1000, 'status': 'pending'
  }
  stub_repo.save_payment.side_effect = lambda p: p
  service = PaymentService(stub_repo)
  result = service.capture('pay_1')
  assert result['status'] == 'succeeded'
```

**Spy test — verify audit logging on payment failure**

Payment failures should be logged for audit purposes. Use a spy to verify the logger is called without replacing its real behaviour.

1. Create a spy on `logger.warn` (or `logger.info`)
2. Call `fail()` with a valid pending payment id
3. Assert the spy was called with a message containing the payment id
4. Call `capture()` with a valid pending payment — assert `logger.warn` was **NOT** called

---

### Task 4 — Route Tests: TDD for the Web Layer

**Technique:** Mocks · supertest / TestClient (Days 5, 6)

Build the HTTP routes. Test each route in isolation by mocking the service layer. No real server. No real service runs inside a route test.

> ⚠️ **Route tests mock the service — always**
> Your route test file mocks the service before any test runs. The route test only checks HTTP behaviour: correct status code, correct response body shape, and whether the service was (or was not) called. Business rules are already tested in Task 2 — don't repeat them here.

**Required route tests — POST `/customers` (4 tests)**

1. Returns `201` and the new customer object on valid input
2. Returns `400` when `name` is missing from the body
3. Returns `400` when `email` is missing from the body
4. `service.createCustomer()` is **NOT** called when input is invalid — verify with a mock assertion

**Required route tests — POST `/payments` (5 tests)**

5. Returns `201` and the payment with status `'pending'` on valid input
6. Returns `400` when `amount` is missing
7. Returns `400` when `currency` is missing
8. Returns `400` when `customerId` is missing
9. Returns `500` with `{ error: 'Something went wrong' }` when service throws unexpectedly

**Required route tests — POST `/payments/:id/capture` (3 tests)**

10. Returns `200` and the updated payment when capture succeeds
11. Returns `404` when payment id is unknown
12. Returns `409` when payment cannot be captured (already succeeded or failed)

**Required route tests — POST `/refunds` (4 tests)**

13. Returns `201` and the refund object on valid input
14. Returns `400` when `paymentId` is missing
15. Returns `400` when `amount` is missing
16. Returns `422` when refund amount exceeds the payment amount

**Required route tests — GET `/payments` (2 tests)**

17. Returns `200` and a list of all payments
18. Returns `500` when service throws unexpectedly

---

### Task 5 — Edge Cases & Error Handling

**Technique:** Boundary values · Not-found paths · 500s (Day 7)

Add the edge-case tests. These are the tests that catch real production bugs in payment systems — and the ones that regulators and security auditors look for.

**Boundary value tests — payment amounts**

Rule: test (boundary − 1), exactly at the boundary, and (boundary + 1) for every constraint.

1. POST `/payments` — amount of `1` (minimum) → `201`
2. POST `/payments` — amount of `0` → `400`
3. POST `/payments` — amount of `-1` → `400`
4. POST `/payments` — amount of `9.99` (decimal) → `400`
5. POST `/refunds` — refund amount equal to payment amount (full refund) → `201`
6. POST `/refunds` — refund amount one penny over the payment amount → `422`

**Boundary value tests — customer name length (100 char limit)**

1. POST `/customers` — name of 1 character → `201`
2. POST `/customers` — name of 100 characters → `201`
3. POST `/customers` — name of 101 characters → `400`

**Not-found tests (404) — one per `:id` endpoint**

4. GET `/customers/:id` — unknown id → `404` + `{ error: 'Customer not found' }`
5. GET `/customers/:id/payments` — unknown customer id → `404` + `{ error: 'Customer not found' }`
6. GET `/payments/:id` — unknown id → `404` + `{ error: 'Payment not found' }`
7. POST `/payments/:id/capture` — unknown id → `404` + `{ error: 'Payment not found' }`
8. POST `/payments/:id/fail` — unknown id → `404` + `{ error: 'Payment not found' }`
9. GET `/refunds/:id` — unknown id → `404` + `{ error: 'Refund not found' }`

**Input variation tests — null, empty, and missing are different**

1. POST `/payments` — no body at all → `400`
2. POST `/payments` — `amount: null` → `400`
3. POST `/payments` — `amount: 0` → `400`
4. POST `/payments` — `currency: ""` (empty string) → `400`
5. POST `/customers` — email with no `@` → `400`
6. POST `/customers` — same email twice → `409` Conflict

**Unexpected failure (500) tests**

7. GET `/payments` — service throws → `500` + `{ error: 'Something went wrong' }`
8. POST `/payments` — service throws after validation passes → `500` + generic message
9. POST `/refunds` — service throws → `500` + generic message

> 🔒 **Payment security — never expose internal errors**
> In payment systems this is critical. A stack trace or database error leaking to a client can expose card data, account structures, or infrastructure details. Always catch, log server-side, and return a safe generic message. Your 500 test should confirm the client only ever sees `{ "error": "Something went wrong" }`.

---

## 5. Getting Started

### 5.1 Setup

**JavaScript — Express + Jest**
```bash
npm init -y
npm install express
npm install --save-dev jest supertest
# package.json:
# "test": "jest --verbose"
```

**Python — FastAPI + pytest**
```bash
pip install fastapi pytest httpx
pip install uvicorn pytest-asyncio
# Run all tests:
pytest tests/ -v
```

### 5.2 Suggested Folder Structure

**JavaScript**
```
payments-api/
  src/
    utils/validators.js          ← Task 1
    services/
      paymentService.js          ← Task 2
    repos/
      fakePaymentRepo.js         ← Task 3
    routes/
      customers.js               ← Task 4
      payments.js
      refunds.js
    app.js
  tests/
    unit/validators.test.js
    services/paymentService.test.js
    repos/fakePaymentRepo.test.js
    routes/customers.test.js
    routes/payments.test.js
    routes/refunds.test.js
  package.json
  README.md
```

**Python**
```
payments_api/
  app/
    utils/validators.py          ← Task 1
    services/
      payment_service.py         ← Task 2
    repos/
      fake_payment_repo.py       ← Task 3
    routes/
      customers.py               ← Task 4
      payments.py
      refunds.py
    main.py
  tests/
    unit/test_validators.py
    services/test_payment_service.py
    repos/test_fake_payment_repo.py
    routes/test_customers.py
    routes/test_payments.py
    routes/test_refunds.py
  conftest.py
  README.md
```

---

## 6. Grading Rubric

100 points total. All listed tests must be present and passing. Partial credit is available within each task.

| Task | Pts | What we look for |
|------|-----|-----------------|
| Task 1 — Validation unit tests | 15 | 16 required tests present. Correct matchers throughout. Each test is independent. |
| Task 2a — PaymentService (22 tests) | 15 | All 22 tests present and passing. Tests inject FakeRepository — no real database. |
| Task 2b — Refactoring (Day 4) | 10 | At least one refactor committed after tests pass. STATUS constants extracted. No tests break. |
| Task 3a — FakeRepository (8 tests) | 10 | All 8 Fake tests present and passing. `clear()` called in `beforeEach`. |
| Task 3b — Stub + Spy tests | 10 | One stub test (capture or fail logic). One spy test on audit logger. Both demonstrate understanding, not just syntax. |
| Task 4 — Route tests (18 tests) | 20 | Service is mocked in all route tests. All HTTP status codes tested including 409 and 422. Mock assertion confirms service is not called on invalid input. |
| Task 5a — Boundary tests | 8 | Amount boundaries (0, 1, negative, decimal). Customer name boundaries (1, 100, 101 chars). Full refund = payment amount (passes). One penny over (fails). |
| Task 5b — Not-found (404) tests | 7 | All 6 `:id` endpoints have a 404 test. Error body contains a clear message naming the resource. |
| Task 5c — 500 + input variation tests | 5 | 3 unexpected-error (500) tests. 6 input-variation tests. Generic message returned to client. |
| **TOTAL** | **100** | All tests green. TDD discipline visible in commit history. Code is clean and well-structured. |

---

## 7. Rules & Tips

### Non-negotiable rules
- **Test first. Always. Every time. No exceptions.**
- No real database in any test. All persistence goes through a Fake or a mock.
- No real HTTP server in route tests. supertest and TestClient run in-process.
- Each test must pass or fail in isolation — order must not matter.
- One concept per test. If the test name contains 'and', split it in two.
- All tests must be green before you submit.

### Tips for the payment domain
- **Amounts are integers.** £29.99 → `2999`. Always. Reject anything that is not a positive integer from the very first test.
- **Status transitions are state machine logic.** Draw the states and arrows first: `pending → succeeded`, `pending → failed`. Nothing else is valid.
- **The over-refund rule is a boundary.** Test amount = payment (passes), amount = payment + 1 (fails). This is exactly a boundary test.
- `409 Conflict` is the right status for duplicate email. It is also right for 'already captured'. `422 Unprocessable` is right for over-refund.
- **The spy on the audit logger is important in payments.** In real systems, every failed payment must be logged. Your spy test proves that.

### What a great submission looks like
- 60+ tests total across all files
- Zero failing tests
- `STATUS` constants object — no raw strings like `'pending'` scattered through the code
- Commit history shows test → implementation → refactor in that order
- Route test files mock the service — never import the real service
- README includes setup, how to run tests, and a reflection paragraph

---

## 8. Submission Checklist

Go through this before submitting your GitHub link.

- [ ] `npm test` (or `pytest`) runs with zero failures
- [ ] Task 1: all 16 validator unit tests present and green
- [ ] Task 2: all 22 PaymentService tests present and green
- [ ] Task 2: STATUS constants extracted. At least one 'refactor' commit after tests went green
- [ ] Task 3: FakeRepository has its own 8 tests. `clear()` called in `beforeEach`
- [ ] Task 3: one stub test (capture/fail) and one spy test (audit logger)
- [ ] Task 4: service is mocked in all route test files — never the real service
- [ ] Task 4: 409 and 422 status codes are tested as well as 200/201/400/404/500
- [ ] Task 5: amount boundary tests — 0, 1, -1, decimal all present
- [ ] Task 5: full refund = payment amount (pass) and one-over (fail) both present
- [ ] Task 5: all 6 `:id` endpoints have a 404 test with a named error message
- [ ] Task 5: three 500 tests — client receives generic message only
- [ ] README: setup instructions, how to run tests, reflection paragraph (≥150 words)
- [ ] Repository is public — verify from a private/incognito browser window

---

*A test that fails is more valuable than a test you never wrote. Good luck.*