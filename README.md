
# Pytest Framework - Quick Start Guide

Welcome to the Pytest Framework! This guide will help you execute test cases efficiently.

---

## Prerequisites

- Ensure Python is installed on your system.  
- Pytest must be installed. Run the following command if Pytest is not already installed:  
  ```bash
  pip install pytest
  ```

---

## How to Execute Test Cases

Follow these steps to execute your test cases:

1. **Open the Terminal:**  
   Open your terminal/command prompt.

2. **Navigate to the Project Directory:**  
   Use the `cd` command to change to the root/project folder where your test cases are located. For example:  
   ```bash
   cd /path/to/your/project
   ```

3. **Run Pytest Command:**  
   Execute the following command to run all test cases:  
   ```bash
   pytest
   ```

---

## Additional Information

- To run tests in a specific file:  
  ```bash
  pytest <test_file_name>.py
  ```

- To see detailed output during the test execution, add the `-v` flag:  
  ```bash
  pytest -v
  ```

- To generate a test report, you can use:  
  ```bash
  pytest --html=report.html
  ```

---

Thank you for using the Pytest Framework! 🎉
