
# Python Virtual Environments (venv)

## 1. Install `venv` (if needed)

Most systems already have the `venv` module installed, but if not:
  
  ```bash
  sudo apt-get install python3-venv
  ```

---

## 2. Create a Virtual Environment

Navigate to the directory where you want to create the virtual environment, then run the following command:

```bash
python3 -m venv your_venv_name
```

Replace `your_venv_name` with the desired name for your virtual environment.

---

## 3. Activate the Virtual Environment

Once created, activate the virtual environment using the following commands:

  ```bash
  source your_venv_name/bin/activate
  ```

After activation, your prompt should look like this:

```bash
(your_venv_name) $
```

---

## 4. Deactivate the Virtual Environment

To deactivate the virtual environment, run the following command:

```bash
deactivate
```
