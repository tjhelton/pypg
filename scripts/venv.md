
# Setting Up a Python Virtual Environment (venv)

## 1. Install Python (if not installed)

Ensure Python is installed by running the following command in your terminal or command prompt:

```bash
python3 --version
```

If Python is not installed, download and install it from [Python's official website](https://www.python.org/downloads/).

---

## 2. Install `venv` (if needed)

Most systems already have the `venv` module installed, but if not:

Linux/Unix**:
  
  ```bash
  sudo apt-get install python3-venv
  ```

---

## 3. Create a Virtual Environment

Navigate to the directory where you want to create the virtual environment, then run the following command:

```bash
python3 -m venv your_venv_name
```

Replace `your_venv_name` with the desired name for your virtual environment.

---

## 4. Activate the Virtual Environment

Once created, activate the virtual environment using the following commands:

  ```bash
  source your_venv_name/bin/activate
  ```

After activation, your prompt should look like this:

```bash
(your_venv_name) $
```

---

## 5. Install Packages in the Virtual Environment

To install packages in your virtual environment, use `pip` as usual. For example:

```bash
pip3 install requests
```

---

## 6. Deactivate the Virtual Environment

To deactivate the virtual environment, run the following command:

```bash
deactivate
```
