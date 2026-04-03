# BDD Assignment: Web Application Functionality Testing

This project demonstrates the application of **Behavior Driven Development (BDD)** principles to test and document the functionalities of three distinct web applications: **broHOSTS**, **broRacks**, and **ocs4dev**.

## 1. What is BDD?
Behavior Driven Development (BDD) is an agile software development process that encourages collaboration between developers, QA, and non-technical stakeholders. It focuses on the **behavior** of the system from the user's perspective rather than the implementation details.

In this exercise, we identified 3 functionalities for each of the 3 webapps and wrote 2 scenarios for each, following the updated lecturer requirements.

## 2. Gherkin: The Language of BDD
Gherkin is the domain-specific language used to write BDD scenarios. It uses a structured format that is human-readable yet machine-executable. The primary keywords are:
- **Feature:** Describes the high-level functionality.
- **Scenario:** A specific example of a behavior.
- **Given:** The initial context or state.
- **When:** The action taken by the user.
- **Then:** The expected outcome or result.

## 3. Tools and Frameworks

### Behave (Python)
In this project, we use **Behave**, a popular BDD framework for Python. It allows us to map Gherkin scenarios (stored in `.feature` files) to Python code (stored in `steps/` directories).

### Playwright vs. Selenium
- **Playwright:** Used in the **broHOSTS** demo of this project. It is a modern, fast, and reliable end-to-end testing tool. It supports auto-waiting, handles modern web architectures (like Shadow DOM), and is generally preferred for its speed and developer-friendly API.
- **Selenium:** A veteran in the industry. While highly flexible and supporting almost every browser/language, it often requires manual wait management and can be slower compared to modern alternatives like Playwright or Cypress.

### BDD Frameworks in Other Languages
BDD is a cross-language philosophy, and most languages have a dedicated framework:
- **Ruby:** **Cucumber** (The original BDD framework).
- **JavaScript/TypeScript:** **Cucumber.js** often paired with **Playwright** or **Cypress**.
- **Java:** **Cucumber-JVM** or **JBehave**.
- **PHP:** **Behat**.
- **C# / .NET:** **SpecFlow** (now Reqnroll).

## 4. How to Run the Tests

Ensure you have the environment set up using `uv`:

```bash
# Run all tests (Placeholders + Live Demo)
uv run behave behave_tests/brohosts behave_tests/broracks behave_tests/ocs4dev

# Run only the live Playwright demo for broHOSTS
uv run behave behave_tests/brohosts
```

*Note: The broHOSTS tests include a live demo with automated browser interactions, while broracks and ocs4dev currently use placeholder steps.*
