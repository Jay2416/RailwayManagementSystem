import pandas as pd
import random as rd 
import mysql.connector as connector
import datetime
import tkinter.filedialog as box
import os
from tkinter import *
from getpass import getpass

def add_database(filename):
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(';')

    for command in sql_commands:
        try:
            if command.strip() != '':
                cur.execute(command)
        except IOError as msg:
            print ("Command skipped: ", msg)
password = getpass("Enter your MySQL password here: ")

try: 
    try: 
        con = connector.connect(host="localhost",
                                user="root",
                                password=password,  #Edit MySQL password here
                                database="railway")
        cur = con.cursor()

    except Exception as e:
        con1 = connector.connect(host="localhost",
                            user="root",
                            password=password)   #Edit MySQL password here
        cur1 = con1.cursor()
        cur1.execute("create database railway")
        con1.commit()
        con1.close()

        con = connector.connect(host="localhost",
                                user="root",
                                password=password,  #Edit MySQL password here
                                database="railway")
        cur = con.cursor()
        Tk().withdraw()
        file = box.askopenfile(mode="r")
        try: 
            if file:
                filepath = os.path.abspath(file.name)
        except Exception as e:
            quit()
        add_database(str(filepath))
        con.commit()

except Exception as e:
    quit()

def error():
    print("Enter Valid Input....")
    print("="*121)
    main_choice()

def train_list():
    cur.execute("select t_no, t_name from train")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Train Number", "Train Name"])
    print(df)
    print("="*121)

def train_station_list():
    cur.execute("select t_no, t_name, station from train_stations")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Train Number", "Train Name", "Train Stations"])
    print(df)
    print("="*121)

def passneger_list():
    cur.execute("select p.pid, t.t_no, p.p_name, t.t_name from passenger p, train t where t.t_no=p.t_no")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Passenger ID", "Train Number", "Passenger Name", "Train Name"])
    print(df)
    print("="*121)

def fare_list():
    cur.execute("select t.t_no, t.t_name from train t, fare f where t.t_no=f.t_no")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Train Number", "Train Name"])
    print(df)
    print("="*121)

def add_train():
    tno = rd.randrange(100000, 999999)
    tname = input("Enter train's name: ")
    arrival = input("Enter train's arrival station: ")
    final = input("Enter train's final destination: ")
    starttime = input("Enter train's starting time: ")
    endtime = input("Enter train's reaching time: ")

    cur.execute(f"insert into train values ({tno}, '{tname}', '{arrival}', '{final}','{starttime}','{endtime}')")
    con.commit()
    print("Inserted Sucessfully!!")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        add_menu()
    else:
        error()

def add_stations():
    cur.execute("select t_no, t_name, starting_station, destination_station from train")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Train Number", "Train Name", "Arrival", "Destination"])
    print(df)
    print("="*121)
    tno = int(input("Enter train number: "))
    cur.execute(f"select t_name from train where t_no={tno}")
    data2 = cur.fetchall()
    tname = data2[0][0]
    station = input("Enter the stations: ")
    cur.execute(f"insert into train_stations values ({tno}, '{tname}', '{station}')")
    con.commit()
    print("Inserted Successfully!!")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        add_menu()
    else:
        error()

def add_passenger():
    train_station_list()
    pid = rd.randrange(100000, 1000000)
    pname = input("Enter your name: ")
    tno = int(input("Enter train number: "))
    arrival = input("Enter arrival station: ")
    destination = input("Enter your destination: ")

    cur.execute(f"select station from train_stations where t_no={tno}")
    stations = cur.fetchall()
    cur.execute(f"select instr('{stations[0][0]}', '{destination}')")
    check = cur.fetchall()
    if check[0][0] == 0:
        print("Please enter the VALID destination....")
        print("="*121)
        main_choice()

    classes = input("Enter the class: ")
    jy_date = datetime.date.today()
    adhar_no = input("Enter the Aadhar No: ")
    if len(adhar_no) != 12:
        print("Enter AADHAR NUMBER of 12 digits....")
        print("="*121)
        main_choice()

    try: 
        cur.execute(f"select fare from fare where t_no={tno} and class='{classes}' and destination='{destination}' and arrival_station='{arrival}'")
        data1 = cur.fetchall()
        fare1 = data1[0][0]
        cur.execute(f"insert into passenger values ('{pid}', '{pname}', {tno}, '{arrival}', '{destination}', '{classes}', '{jy_date}', '{adhar_no}', {fare1})")
        con.commit()
        print("Inserted Successfully!!")
        print("="*121)

    except Exception as e:
        try:
            cur.execute(f"select fare from fare where t_no={tno} and class='{classes}' and destination='{arrival}' and arrival_station='{destination}'")
            data2 = cur.fetchall()
            fare2 = data2[0][0]
            cur.execute(f"insert into passenger values ('{pid}', '{pname}', {tno}, '{arrival}', '{destination}', '{classes}', '{jy_date}', '{adhar_no}', {fare2})")
            con.commit()
            print("Inserted Successfully!!")
        except Exception as e:
            print("Enter VALID details....")
            print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        add_menu()
    else:
        error()

def add_fare():
    try:
        train_station_list()
        tno = int(input("Enter train number: "))
        arrival_ask = input("Enter the arrival station: ")
        cur.execute(f"select station from train_stations where t_no={tno}")
        check1 = cur.fetchall()
        stations = check1[0][0]
        cur.execute(f"select instr('{stations}', '{arrival_ask}')")
        check = cur.fetchall()
        if check[0][0] == 0:
            print("Please enter VALID arrival")
            print("="*121)
            add_menu()
        destination = input("Enter the destination: ")
        cur.execute(f"select station from train_stations where t_no={tno}")
        check1 = cur.fetchall()
        stations = check1[0][0]
        cur.execute(f"select instr('{stations}', '{destination}')")
        check = cur.fetchall()
        if check[0][0] == 0:
            print("Please enter VALID destination")
            print("="*121)
            add_menu()
        ask_class = input("Enter the class: ")
        fare = int(input("Enter the fare(in Rs.): "))

        cur.execute(f"insert into fare values ({tno}, '{arrival_ask}', '{destination}', '{ask_class}', {fare})")
        con.commit()
        print("Inserted Successfully!!")

        var = input("Do you want to continue(y/n): ")
        print("="*121)
        if var == "N" or var == "n":
            main_choice()
        elif var == "Y" or var == "y":
            add_menu()
        else:
            error()

    except Exception as e:
        error()

def add_menu():
    print("                                 Firstly fill the train details for proper functioning of program.                                            ")
    print("                                                   Please move in sequence.                                                ")
    print("1. To add train details.")
    print("2. To add stations details.")
    print("3. To add new passenger.")
    print("4. To add fare.")
    print("0. To exit.")
    print("="*121)

    ask = input("Enter your choice: ")
    print("="*121)

    if ask == "1":
        add_train()
    elif ask == "2":
        add_stations()
    elif ask == "3":
        add_passenger()
    elif ask == "4":
        add_fare()
    elif ask == "0":
        main_choice() 
    else:
        print("Enter Valid Input...")
        print("="*121)
        add_menu()

def del_train():
    try:
        cur.execute("select * from train")
        data1 = cur.fetchall()
        train_list()
        del_tno = int(input("Enter the train number: "))
        cur.execute(f"delete from train where t_no={del_tno}")
        con.commit()

        cur.execute("select * from train")
        data2 = cur.fetchall()

        if data1 == data2:
            print("Please Enter VALID data to delete....")
            print("="*121)
            main_choice()
        else:
            print("Data Deleted Successfully!!")
            print("="*121)

        var = input("Do you want to continue(y/n): ")
        print("="*121)
        if var == "N" or var == "n":
            main_choice()
        elif var == "Y" or var == "y":
            delete_menu()
        else:
            error()

    except Exception as e:
        print("Please enter VALID train number to delete the record....")
        print("="*121)
        main_choice()

def del_train_stations():
    cur.execute("select * from train_stations")
    data1 = cur.fetchall()
    train_station_list()
    del_tno = int(input("Enter the train number: "))
    cur.execute(f"delete from train_stations where t_no={del_tno}")
    con.commit()

    cur.execute("select * from train_stations")
    data2 = cur.fetchall()

    if data1 == data2:
        print("Please Enter VALID data to delete....")
        print("="*121)
        main_choice()

    else:
        print("Data Deleted Successfully!!")
        print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        delete_menu()
    else:
        error()

def del_passenger():
    cur.execute("select * from passenger")
    data1 = cur.fetchall()
    passneger_list()
    del_tno = int(input("Enter the train number: "))
    del_pid = int(input("Enter the passenger id: "))
    cur.execute(f"delete from passenger where t_no={del_tno} and pid='{del_pid}'")
    con.commit()

    cur.execute("select * from passenger")
    data2 = cur.fetchall()

    if data1 == data2:
        print("Please Enter VALID data to delete....")
        print("="*121)
        main_choice()

    else:
        print("Data Deleted Successfully!!")
        print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        delete_menu()
    else:
        error()

def del_fare():
    cur.execute("select * from fare")
    data1 = cur.fetchall()
    fare_list()
    del_tno = int(input("Enter the train number: "))
    cur.execute(f"delete from fare where t_no={del_tno}")
    con.commit()

    cur.execute("select * from fare")
    data1 = cur.fetchall()

    if data1 == data2:
        print("Please Enter VALID data to delete....")
        print("="*121)
        main_choice()

    else:
        print("Data Deleted Successfully!!")
        print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        delete_menu()
    else:
        error()

def delete_menu():
    print("1. To delete train details.")
    print("2. To delete stations details.")
    print("3. To delete passenger.")
    print("4. To delete fare.")
    print("0. To exit.")
    print("="*121)

    ask = input("Enter Your Choice: ")
    print("="*121)

    if ask == "1":
        del_train()
    elif ask == "2":
        del_train_stations()
    elif ask == "3":
        del_passenger()
    elif ask == "4":
        del_fare()
    elif ask == "0":
        main_choice()
    else:
        print("Enter Valid Input....")
        print("="*121)
        delete_menu()

def update_train():
    train_list()
    tno_ask = input("Enter train number: ")
    print("="*121)

    print("1. To update train name.")
    print("2. To update initial station of train.")
    print("3. To update final station of train.")
    print("4. To update arrival time of train.")
    print("5. To update reaching time of train.")
    print("0. To exit.")
    print("="*121)
    
    ask = input("Enter Your Choice: ")
    print("="*121)

    try:
        if ask == "1":
            new_ask = input("Enter the new train name: ")
            cur.execute(f"update train set t_name='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "2":
            new_ask = input("Enter the new initial station of the train: ")
            cur.execute(f"update train set starting_station='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "3":
            new_ask = input("Enter the new final station of the train: ")
            cur.execute(f"update train set starting_station='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "4":
            new_ask = input("Enter the new arrival time of the train: ")
            cur.execute(f"update train set starting_station='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "5":
            new_ask = input("Enter the new reaching time of the train: ")
            cur.execute(f"update train set destination_station='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "0":
            main_choice()
        else:
            print("Enter Valid Input....")
            print("="*121)
            update_data()
    
    except Exception as e:
        print("Please check that the data entered is VALID.")
        print("="*121)
        update_data()


def update_stations():
    train_station_list()
    tno_ask = input("Enter train number: ")
    print("="*121)

    print("1. To update train number.")
    print("2. To update train name.")
    print("3. To update train stations.")
    print("0. To exit.")    
    print("="*121)

    ask = input("Enter Your Choice: ")
    print("="*121)

    try:
        if ask == "1":
            new_ask = int(input("Enter the new train number: "))
            cur.execute(f"update train_stations set t_no={new_ask} where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "2":
            new_ask = input("Enter the new train name: ")
            cur.execute(f"update train_stations set t_name='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "3":
            new_ask = input("Enter the new train stations: ")
            cur.execute(f"update train_stations set station='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "0":
            main_choice()
        else:
            print("Enter Valid Input....")
            print("="*121)        
            update_data()

    except Exception as e:
        print("Please check that the data entered is VALID.")
        print("="*121)
        update_data()

def update_passenger():
    passneger_list()
    tno_ask = input("Enter train number: ")
    pid_ask = int(input("Enter the passenger id: "))
    print("="*121)

    print("1. To update passenger name.")
    print("2. To update train number.")
    print("3. To update arrival.")
    print("4. To update destination.")
    print("5. To update class.")
    print("6. To update journey date.")
    print("7. To update aadhar number.")
    print("8. To update fare.")
    print("0. To exit.")    
    print("="*121)

    ask = input("Enter Your Choice: ")
    print("="*121)

    try: 
        if ask == "1":
            new_ask = input("Enter the new passenger name: ")
            cur.execute(f"update passenger set p_name='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "2":
            new_ask = input("Enter the new train number: ")
            cur.execute(f"update passenger set t_no={new_ask} where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "3":
            new_ask = input("Enter the new arrival: ")
            cur.execute(f"update passenger set arrival='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "4":
            new_ask = input("Enter the new destination: ")
            cur.execute(f"update passenger set destination='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "5":
            new_ask = input("Enter the new class: ")
            cur.execute(f"update passenger set class='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "6":
            new_ask = input("Enter the new journey date: ")
            cur.execute(f"update passenger set jy_date='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "7":
            new_ask = input("Enter the new aadhar number: ")
            cur.execute(f"update passenger set adhar_no='{new_ask}' where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "8":
            cur.execute(f"select class, destination, arrival from passenger where t_no={tno_ask} and pid='{pid_ask}'")
            data1 = cur.fetchall()
            classes = data1[0][0]
            destination = data1[0][1]
            arrival = data1[0][2]

            cur.execute(f"select fare from fare where t_no={tno_ask} and class='{classes}' and destination='{destination}' and arrival_station='{arrival}'")
            data2 = cur.fetchall()
            fare = data2[0][0]

            if data2 == []:
                cur.execute(f"select fare from fare where t_no={tno} and class='{classes}' and destination='{arrival}' and arrival_station='{destination}'")
                con.commit()
                print("Inserted Successfully!!")

            cur.execute(f"update passenger set fare={fare} where t_no={tno_ask} and pid='{pid_ask}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "0":
            main_choice()
        else:
            print("Enter Valid Input....")
            print("="*121)        
            update_data()

    except Exception as e:
        print("Please check that the data entered is VALID.")
        print("="*121)
        update_data()

def update_fare():
    cur.execute("select t.t_no, t.t_name, f.arrival_station, f.destination, f.class, f.fare from train t, fare f where t.t_no=f.t_no")
    x = cur.fetchall()
    df = pd.DataFrame(x, columns=["Train Number", "Train Name", "Arrival", "Destination", "Class", "Fare"])
    print(df)
    print("="*121)
    tno_ask = input("Enter train number: ")
    print("="*121)

    print("1. To update train number.")
    print("2. To update arrival station.")
    print("3. To update destination.")
    print("4. To update class.")
    print("5. To update fare.")
    print("0. To exit.")    
    print("="*121)

    ask = input("Enter Your Choice: ")
    print("="*121)

    try: 
        if ask == "1":
            new_ask = int(input("Enter the new train number: "))
            cur.execute(f"update fare set t_no={new_ask} where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "2":
            new_ask = int(input("Enter the new arrival station: "))
            confirm1 = input("Enter the destination of the train: ")
            confirm2 = input("Enter the class of the train: ")
            cur.execute(f"select station from train_stations where t_no={tno_ask}")
            check1 = cur.fetchall()
            stations = check1[0][0]
            cur.execute(f"select instr('{stations}', '{new_ask}')")
            check = cur.fetchall()
            if check[0][0] == 0:
                print("Please enter VALID arrival")
                print("="*121)
                add_menu()
            cur.execute(f"update fare set arrival_station='{new_ask}' where t_no={tno_ask} and destination='{confirm1}' and class='{confirm2}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "3":
            new_ask = input("Enter the new destination: ")
            confirm1 = input("Enter the arrival of the train: ")
            confirm2 = input("Enter the class of the train: ")
            cur.execute(f"select station from train_stations where t_no={tno_ask}")
            check1 = cur.fetchall()
            stations = check1[0][0]
            cur.execute(f"select instr('{stations}', '{new_ask}')")
            check = cur.fetchall()
            if check[0][0] == 0:
                print("Please enter VALID destination")
                print("="*121)
            cur.execute(f"update fare set destination='{new_ask}' where t_no={tno_ask} and arrival_station='{confirm1}' and class='{confirm2}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "4":
            new_ask = input("Enter the new class: ")
            cur.execute(f"update fare set class='{new_ask}' where t_no={tno_ask}")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "5":
            new_ask = input("Enter the new fare: ")
            confirm1 = input("Enter the arrival of the train: ")
            confirm2 = input("Enter the destination of the train: ")
            confirm3 = input("Enter the class of the train: ")
            cur.execute(f"update fare set fare={new_ask} where t_no={tno_ask} and arrival_station='{confirm1}' and destination='{confirm2}' and class='{confirm3}'")
            con.commit()
            print("Updated Successfully!!")
            print("="*121)

            var = input("Do you want to continue(y/n): ")
            print("="*121)
            if var == "N" or var == "n":
                main_choice()
            elif var == "Y" or var == "y":
                update_data()
            else:
                error()
        elif ask == "0":
            main_choice()
        else:
            print("Enter Valid Input....") 
            print("="*121)
            update_data()

    except Exception as e:
        print("Please check that the data entered is VALID.")
        print("="*121)
        update_data()

def update_data():
    print("1. To update train details.")
    print("2. To update stations details.")
    print("3. To update passenger.")
    print("4. To update fare.")
    print("0. To exit.")
    print("="*121)

    ask = input("Enter Your Choice: ")
    print("="*121)

    if ask == "1":
        update_train()
    elif ask == "2":
        update_stations()
    elif ask == "3":
        update_passenger()
    elif ask == "4":
        update_fare()
    elif ask == "0":
        main_choice()
    else:
        print("Enter Valid Input...")
        print("="*121)
        update_data()

def show_train():
    cur.execute("select * from train")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["Train No","Train Name","Arrival Station","Destination","Arrival Time","Reaching Time"])
    print(f"Your train details are:\n{df}")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        show_details()
    else:
        error()

def show_stations():
    cur.execute("select * from train_stations")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["Train No", "Train Name", "Stations"])
    print(f"Your train station details are:\n{df}")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        show_details()
    else:
        error()

def show_passenger():
    cur.execute("select * from passenger")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["Passenger ID", "Passenger Name", "Train Number", "Arrival", "Destination", "Class", "Journey Date", "Adhar Number", "Fare"])
    print(f"Your train station details are:\n{df}")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        show_details()
    else:
        error()

def show_fare():
    cur.execute("select * from fare")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["Train No", "Arrival Station", "Destination", "Class", "Fare(in Rs.)"])
    print(f"Your train station details are:\n{df}")
    print("="*121)

    var = input("Do you want to continue(y/n): ")
    print("="*121)
    if var == "N" or var == "n":
        main_choice()
    elif var == "Y" or var == "y":
        show_details()
    else:
        error()

def show_details():
    print("1. To see train details.")
    print("2. To see stations details.")
    print("3. To see passenger.")
    print("4. To see fare.")
    print("0. To exit.")
    print("="*121)

    ask = input("Enter Your Choice: ")
    if ask == "1":
        show_train()
    elif ask == "2":
        show_stations()
    elif ask == "3":
        show_passenger()
    elif ask == "4":
        show_fare()
    elif ask == "0":
        main_choice()
    else:
        print("Enter Valid Input....")
        print("="*121)
        show_details()

def display_ticket():
    cur.execute(f"select pid, p_name from passenger")
    data1 = cur.fetchall()
    df = pd.DataFrame(data1, columns=["Passenger ID", "Passenger Name"])
    print(df)
    print("="*121)
    pid_ask = int(input("Enter the passenger id: "))

    cur.execute(f"select p.p_name, t.t_no, t.t_name, p.arrival, p.destination, p.class, p.jy_date, fare from passenger p, train t where p.t_no=t.t_no and p.pid={pid_ask}")
    data = cur.fetchall()
    df1 = pd.DataFrame(data)
    df2 = df1.T
    df2.index = ["Passenger Name", "Train Number", "Train Name", "Arrival Station", "Destination", "Class", "Journey Date", "Fare(in Rs.)"]
    df2.columns= ["Ticket"]
    print(df2)
    print("="*121)

    main_choice()

print()
print("*************************************************************************************************************************")
print("*                                              RAILWAY MANAGEMENT SYSTEM                                                *")
print("*************************************************************************************************************************")

def main_choice():
    print("1. Add data[Train & Passenger]")
    print("2. Remove data[Train & Passenger]")
    print("3. Modify data[Train & Passenger]")
    print("4. Display Details[Train & Passenger]")
    print("5. Display Ticket of Passenger")
    print("0. To Exit the program")
    print("="*121)

    main_ask = input("Enter Your Choice: ")
    print("="*121)

    if main_ask == "1":
        add_menu()
    elif main_ask == "2":
        delete_menu()
    elif main_ask == "3":
        update_data()
    elif main_ask == "4":
        show_details()
    elif main_ask == "5":
        display_ticket()
    elif main_ask == "0":
        print("Thank You....\nHave a Nice Day!!\U0001F601")
        quit()
    else:
        print("Enter Valid Input....")
        print("="*121)
        main_choice()

main_choice()
