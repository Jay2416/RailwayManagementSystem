
# Railway Management System

The objective of this project is to develop a computerized MIS to automate the functions of a RAILWAY MANAGEMENT SYSTEM. 

This software project is also aimed to enhance the current record keeping
system, which will help managers to retrieve the up-to-date information at
right time in right shape.
## Tech Stack

**Front-End:** Python

**Back-End:** MySQL


## Features

- If the database of railway is not made then too we can proceed by selecting the `railway.sql` which has certain dummy records in it.
- Provide a user friendly, Command User Interface (CUI) which has integrated and centralized environment for MIS activities.



## Modules Used

- **random**
- **datetime**
- **os**
- **tkinter**
- **pandas**, to install it, use the following command on your command prompt

```bash
  pip install pandas
```

- **mysl-connector**, to install it, use the following command on your command prompt. You can use an alternative module **pymysql** to is getting an error while importing it.

```bash
pip install mysql-connector
pip install pymysql
```
    
## How to convert .py to.exe
By converting into a executable file, you can run this program on any computer irrespective the system has python installed or not. 

You can convert this project(.py) into a executable file(.exe) by following the steps mentioned: 

- Open the command prompt and run command given below.
- First command to make both.exe file with MicroSoft Installer(MSI) setup. 
- Second command to make only .exe file.
```bash
setup.py bsdit_msi
setup.py build
```

**Note:** 
- All the files must be in the same directory.
- CX_Freeze module must be installed. To install it write the following command on your command prompt.

```bash
pip install cx_freeze
```
## Limitations

Despite of the best effort of the developer, the following limitations and
functional boundaries are visible, which limits the scope of this project:

- A train can only have at most three-stopping station.
- We must have to create all the fare and station details after adding a new train in the train table.

