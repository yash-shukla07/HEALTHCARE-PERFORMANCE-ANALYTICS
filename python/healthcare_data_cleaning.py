import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# DATA LOADING
appointments=pd.read_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\1appointments.csv")
billing=pd.read_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\2billing.csv")
doctors=pd.read_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\3doctors.csv")
patients=pd.read_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\4patients.csv")
treatments=pd.read_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\5treatments.csv")

print ("data loaded succesfully")
print(appointments,"\n")
print(billing,"\n")
print(doctors,"\n")
print(patients,"\n")
print(treatments,"\n")


 #DATA INSPECTION
print ("DATA INFORMATION","\n")
print(appointments.info(),"\n")
print(billing.info(),"\n")
print(doctors.info(),"\n")
print(patients.info(),"\n")
print(treatments.info(),"\n")

print ("DATA DESCRIBE")
print(appointments.describe(),"\n")
print(billing.describe(),"\n")
print(doctors.describe(),"\n")
print(patients.describe(),"\n")
print(treatments.describe(),"\n")

print ("DATA TYPES")
print(appointments.dtypes,"\n")
print(billing.dtypes,"\n")
print(doctors.dtypes,"\n")
print(patients.dtypes,"\n")
print(treatments.dtypes,"\n")

print("NULL VALUES","\n")
print(appointments.isnull().sum(),"\n")
print(billing.isnull().sum(),"\n")
print(doctors.isnull().sum(),"\n")
print(patients.isnull().sum(),"\n")
print(treatments.isnull().sum(),"\n")


print("DUPLICATE COUNT","\n")
print(appointments.duplicated().sum(),"\n")
print(billing.duplicated().sum(),"\n")
print(doctors.duplicated().sum(),"\n")
print(patients.duplicated().sum(),"\n")
print(treatments.duplicated().sum(),"\n")

# STRING COLOUM CLEANING 
appointments.columns=appointments.columns.str.lower().str.strip().str.replace(" ","_")
billing.columns=billing.columns.str.lower().str.strip().str.replace(" ","_")
doctors.columns=doctors.columns.str.lower().str.strip().str.replace(" ","_")
patients.columns=patients.columns.str.lower().str.strip().str.replace(" ","_")
treatments.columns=treatments.columns.str.lower().str.strip().str.replace(" ","_")

# DATA TYPE CONVERSION 

# CONVERSION TO DATE TIME
appointments["appointment_date"]=pd.to_datetime(appointments["appointment_date"],format="%d-%m-%Y",errors="coerce")
appointments["appointment_time"]=pd.to_datetime(appointments["appointment_time"],format="%H:%M:%S",errors="coerce").dt.time
billing["bill_date"]=pd.to_datetime(billing["bill_date"],format="%d-%m-%Y",errors="coerce")
patients["date_of_birth"]=pd.to_datetime(patients["date_of_birth"],format="%d-%m-%Y",errors="coerce")
patients["registration_date"]=pd.to_datetime(patients["registration_date"],format="%d-%m-%Y",errors="coerce")
treatments["treatment_date"]=pd.to_datetime(treatments["treatment_date"],format="%d-%m-%Y",errors="coerce")

#  CONVERSION TO STRING 
doctors["phone_number"]=doctors["phone_number"].astype(str)
patients["contact_number"]=patients["contact_number"].astype(str)

# DATA TYPE CHECKING AFTER CONVERSION
print ("DATA TYPES:","\n")
print(appointments.dtypes,"\n")
print(billing.dtypes,"\n")
print(doctors.dtypes,"\n")
print(patients.dtypes,"\n")
print(treatments.dtypes,"\n")
print(patients["contact_number"].head(10))
print(appointments["appointment_time"].head(10))

# NAT COUNT CHECKING AFTER CONVERSION 
print("NaT COUNTS AFTER CONVERSION","\n")
print(appointments["appointment_date"].isna().sum())
print(billing["bill_date"].isna().sum())
print(patients["date_of_birth"].isna().sum())
print(patients["registration_date"].isna().sum())
print(treatments["treatment_date"].isna().sum())
print((billing["amount"] == treatments["cost"]).all())

# STORING CLEANED CSV FILE IN SAME FOLDER
appointments.to_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\cleaned_appointments.csv", index=False)
billing.to_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\cleaned_billing.csv", index=False)
doctors.to_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\cleaned_doctors.csv", index=False)
patients.to_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\cleaned_patients.csv", index=False)
treatments.to_csv(r"C:\Users\shukl_wmeshqg\OneDrive\Desktop\health care data\cleaned_treatments.csv", index=False)

from sqlalchemy import create_engine

# Replace 'your_password' with your actual MySQL root password
engine = create_engine("mysql+mysqlconnector://root:2006@localhost/hospital_db")


patients.to_sql("patients", engine, if_exists="append", index=False)
doctors.to_sql("doctors", engine, if_exists="append", index=False)
appointments.to_sql("appointments", engine, if_exists="append", index=False)
treatments.to_sql("treatments", engine, if_exists="append", index=False)
billing.to_sql("billing", engine, if_exists="append", index=False)

print("Data exported to MySQL successfully")