# Advanced Algebra Final Project
This repository contains the codebase for the final project of `Advanced Algebra` course at Bar-Ilan University (2025).<br><br>
It implements key mathematical concepts and algorithms related to finite fields, discrete logarithms, and field element operations.<br>
Central to the project is the Baby-Step Giant-Step (BSGS) algorithm, which efficiently solves the discrete logarithm problem in finite fields using a time-memory tradeoff.<br><br>
The `FiniteField` class models finite field extensions over prime fields defined by irreducible polynomials, enabling efficient group embeddings and element operations like addition, multiplication, and inversion.<br>
A task manager orchestrates the execution of complex field operations, utilizing abstraction to perform a range of mathematical computations and generate detailed logs for analysis and validation.


## 📋 Repo Components:

| Component         | Description                                                          |
| ----------------- | -------------------------------------------------------------------- |
| [field_elements](https://github.com/GalSarid21/advanced-algebra-biu/tree/main/src/field_elements/abstract_field_element.py) | Implements prime and finite field elements |
| [fields](https://github.com/GalSarid21/advanced-algebra-biu/tree/main/src/fields/finite_field.py) | Defines and operates on finite fields |
| [task_manager](https://github.com/GalSarid21/advanced-algebra-biu/tree/main/task_manager/task_manager.py) | Manages and executes structured assignment sections (as tasks) |
| [data](https://github.com/GalSarid21/advanced-algebra-biu/tree/main/data/second_section.yaml) |Stores configuration and parameters for task execution |
| [common](https://github.com/GalSarid21/advanced-algebra-biu/tree/main/common/entities.py) | Contains shared utilities and logic used across modules |


## ⚙️ Set Python Environment:
1. Make sure you have python version >= 3.10 on your machine:
```python
python --version
```

* If your version doesn't meet the above requirements, download a newer version from python.org (windows) or run `brew upgrade python` on terminal (mac).

2. Clone the project.

3. Open project's main folder (advanced-algebra-biu).

4. Create a virtual environment under a new `venv` folder:
```python
python -m venv ./venv
```

5. Activate the new environment:
```bash
source ./venv/bin/activate
```

* When the `venv` is activated, its name should appear in brackets at the beginning of your terminal prompt. For example:
```bash
saridg@mobl advanced-algebra-biu %
(venv) saridg@mobl advanced-algebra-biu %
```

6. Optional (if running in IDE): set new created python interpreter as IDE interpreter:<br>
&ensp;6.1 On VSCode:<br>
&emsp;&emsp;6.1.1 Open VS Code.<br>
&emsp;&emsp;6.1.2 Press Ctrl + Shift + P (Cmd + Shift + P on Mac) to open the Command Palette.<br>
&emsp;&emsp;6.1.3 Search for "Python: Select Interpreter" and select it.<br>
&emsp;&emsp;6.1.4 Choose the desired Python interpreter from the list (e.g., python3, venv, or a conda env).<br>
&ensp;6.2 On PyCharm:<br>
&emsp;&emsp;6.2.1 Open PyCharm and go to File > Settings (Ctrl + Alt + S on Windows/Linux, Cmd + , on Mac).<br>
&emsp;&emsp;6.2.2 Navigate to Project: <your_project> > Python Interpreter.<br>
&emsp;&emsp;6.2.3 Click the gear icon and choose Add Interpreter.<br>
&emsp;&emsp;6.2.4 Select System Interpreter, Virtualenv, or Conda, and set the correct Python path.<br>
&emsp;&emsp;6.2.5 Click OK/Apply to save changes.<br>

7. Pip-install the project packages using `requirements.txt` file:
```pip
pip install -r requirements.txt
```


## 🏃 Running Assignment Sections (Tasks) Locally:

1. Running the project is possible using a simple cli command:
```python
python main.py --task section-2
```

2. Supported cli arguments:
```description
-- task: An assignment section to run.
* tasks: [
    section-2: test `PrimeFieldElement` (creation + basic functionality).
    section-3: test `FiniteField` and `FiniteFieldElement` (creation + field/field element connection).
    section-4: test element's image calculation.
    section-5: test `FiniteFieldElement` (`pretty_printing` + basic functionality).
    section-6: test `exp_by_squaring` function (exponentiation by squaring algorithm implementation).
    section-7: test `mul_order` function (calculating multiplicative order).
    section-8: test `find_generator` function (finding a generator of a prime field).
    section-9: test `discrete_log_bsgs` function (calculating a discrete log using the baby-step giant-step algorithm).
    section-10: test `discrete_log_lifting` function (calculating discrete log over U_{p^s} and "lift" it to Z_{p}).
    run-all: run all the implemented sections.
]
```


## 🐳 Running Assignment Sections (Tasks) With Docker Container:
1. Make sure you have a docker installation on your machine:
```bash
docker --version
```

* If Docker is not installed or outdated, download the latest version from docker.com (windows) or run brew install --cask docker on terminal (mac).

2. Pull public image:
```bash
docker pull saridga/biu:advanced-algebra
```

* You can tag it with a shorter name for convenience:
```bash
docker tag saridga/biu:advanced-algebra advanced-algebra:latest
```

3. Set local directory for output log files:
```bash
export LOG_DIR=/path/to/local/folder
```

4. Run a container using the pulled image and `LOG_DIR`:
```bash
docker run --rm -v ${LOG_DIR}:/app/logs -e TASK=run-all advanced-algebra
```

* You can target any specific task you want using the docker environment variable `TASK`.<br>
* Once the process run completes, the container should be removed, and `LOG_DIR` should contain a new log file.


## 📤 Outputs:

1. The task manager generates a log file stored in the `logs` directory (created at runtime if not exists).

2. The log file consolidates all the section test results.

3. The log filename follows the format `app_yyyyMMdd_uuid.log`, where `yyyyMMdd` represents the run date, and a unique UUID ensures a new file is created for each execution.

4. Example log file (Section 2 results):
```bash
================================================ Environment Setup ================================================
Environment Variables:
{
    "task": "section-2"
}
======================================== Start executing SecondSectionTask ========================================
Element 0: 0 (P=13 | a_orig=13)
Element 1: 5 (P=13 | a_orig=5)
Element 2: 7 (P=13 | a_orig=7)
Element 3: 1 (P=13 | a_orig=1)
Element 4: 3 (P=11 | a_orig=3)

Addition (e1+e0): 5
Addition (e1+e2): 12
Addition (e2+e2): 1
Error:
Operation 'add' requires both operands to be GF(13) arrays, not [GF(1, order=13), GF(3, order=11)].
Addition (e3+e4): OPERATION FAILED (error message above)

Subtraction (e1-e0): 5
Subtraction (e1-e2): 11
Subtraction (e2-e2): 0
Error:
Operation 'subtract' requires both operands to be GF(13) arrays, not [GF(1, order=13), GF(3, order=11)].
Subtraction (e3-e4): OPERATION FAILED (error message above)

Multiplication (e1*e0): 0
Multiplication (e1*e2): 9
Multiplication (e2*e2): 10
Error:
Operation 'add' requires both operands to be GF(11) arrays, not [GF(3, order=11), 13].
Multiplication (e3*e4): OPERATION FAILED (error message above)

Error:
Cannot compute the multiplicative inverse of 0 in a Galois field.
Division (e1/e0): OPERATION FAILED (error message above)
Division (e1/e2): 10
Division (e2/e2): 1
Error:
Operation 'divide' requires both operands to be GF(13) arrays, not [GF(1, order=13), GF(3, order=11)].
Division (e3/e4): OPERATION FAILED (error message above)

Equality (e1==e0): False
Equality (e1==e2): False
Equality (e2==e2): True
Equality (e3==e4): False

Error:
Cannot compute the multiplicative inverse of 0 in a Galois field.
Inversion (~e0): OPERATION FAILED (error message above)
Inversion (~e1): 8
Inversion (~e2): 2
Inversion (~e3): 1
Inversion (~e4): 4
==================================================================================================================
```
