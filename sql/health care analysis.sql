# HOSPITAL ANALYTICS PROJECT — SQL ANALYSIS
# DATABASE: HOSPITAL_DB
# TABLES: PATIENTS, DOCTORS, APPOINTMENTS, TREATMENTS, BILLING
 
#create database hospital_db;
use hospital_db;
 
# TABLE CREATION (RELATIONAL SCHEMA WITH PRIMARY/FOREIGN KEYS)
 
/*create table patients (
    patient_id varchar(20) primary key,
    first_name varchar(50),
    last_name varchar(50),
    gender varchar(10),
    date_of_birth date,
    contact_number varchar(15),
    address varchar(255),
    registration_date date,
    insurance_provider varchar(100),
    insurance_number varchar(50),
    email varchar(100)
);
 
create table doctors (
    doctor_id varchar(20) primary key,
    first_name varchar(50),
    last_name varchar(50),
    specialization varchar(100),
    phone_number varchar(15),
    years_experience int,
    hospital_branch varchar(100),
    email varchar(100)
);
 
create table appointments (
    appointment_id varchar(20) primary key,
    patient_id varchar(20),
    doctor_id varchar(20),
    appointment_date date,
    appointment_time time,
    reason_for_visit varchar(255),
    status varchar(20),
    foreign key (patient_id) references patients(patient_id),
    foreign key (doctor_id) references doctors(doctor_id)
);
 
create table treatments (
    treatment_id varchar(20) primary key,
    appointment_id varchar(20),
    treatment_type varchar(100),
    description varchar(255),
    cost decimal(10,2),
    treatment_date date,
    foreign key (appointment_id) references appointments(appointment_id)
);
 
create table billing (
    bill_id varchar(20) primary key,
    patient_id varchar(20),
    treatment_id varchar(20),
    bill_date date,
    amount decimal(10,2),
    payment_method varchar(50),
    payment_status varchar(20),
    foreign key (patient_id) references patients(patient_id),
    foreign key (treatment_id) references treatments(treatment_id)
);*/
 
# QUICK DATA CHECK
 
select * from appointments;
select * from billing;
select * from doctors;
select * from patients;
select * from treatments;
 
# SECTION 1: APPOINTMENT ANALYSIS
 
# TOTAL PATIENTS BY REASON FOR VISIT
select
reason_for_visit,
count(patient_id) as patient_count
from appointments
group by reason_for_visit
order by patient_count desc;
 
# APPOINTMENT COUNT BY STATUS
select
status,
count(appointment_id) as appointment_count
from appointments
group by status;
 
# APPOINTMENT COUNT PER MONTH (CHRONOLOGICALLY ORDERED)
select
monthname(appointment_date) as month_name,
count(appointment_id) as total_appointments
from appointments
group by monthname(appointment_date), month(appointment_date)
order by month(appointment_date);
 
# TOTAL APPOINTMENTS PER DOCTOR
select
d.doctor_id,
d.first_name,
d.last_name,
count(a.appointment_id) as total_appointments
from doctors d
left join appointments a on d.doctor_id = a.doctor_id
group by d.doctor_id, d.first_name, d.last_name
order by total_appointments desc;
 
# TREATMENT TYPE RANKED BY NUMBER OF APPOINTMENTS
select
t.treatment_type,
count(a.appointment_id) as total_appointments,
dense_rank() over (order by count(a.appointment_id) desc) as ranking
from treatments t
left join appointments a on t.appointment_id = a.appointment_id
group by t.treatment_type
order by ranking;
 
# APPOINTMENTS BY PATIENT GENDER
select
p.gender,
count(a.appointment_id) as total_appointments
from patients p
left join appointments a on a.patient_id = p.patient_id
group by p.gender
order by total_appointments desc;
 
# HOSPITAL BRANCH RANKED BY TOTAL APPOINTMENTS
select
d.hospital_branch,
count(a.appointment_id) as total_appointments,
dense_rank() over (order by count(a.appointment_id) desc) as ranking
from doctors d
left join appointments a on a.doctor_id = d.doctor_id
group by d.hospital_branch
order by ranking;
 
# NO-SHOW RATE BY HOSPITAL BRANCH
select
    d.hospital_branch,
    count(case when a.status = 'No-show' then 1 end) as no_shows,
    count(a.appointment_id) as total_appointments,
    round(count(case when a.status = 'No-show' then 1 end) * 100.0 / count(a.appointment_id), 2) as no_show_rate_pct
from doctors d
left join appointments a on d.doctor_id = a.doctor_id
group by d.hospital_branch
order by no_show_rate_pct desc;
 
 
# DOCTOR SPECIALIZATION DISTRIBUTION
select
specialization,
count(doctor_id) as doctor_count
from doctors
group by specialization
order by doctor_count desc;
 
# AVERAGE YEARS OF EXPERIENCE BY SPECIALIZATION
select
specialization,
round(avg(years_experience), 1) as avg_years_experience
from doctors
group by specialization
order by avg_years_experience desc;
 
# APPOINTMENTS BY DAY OF WEEK (IDENTIFIES BUSIEST WEEKDAYS)
select
dayname(appointment_date) as day_of_week,
count(appointment_id) as total_appointments
from appointments
group by dayname(appointment_date), dayofweek(appointment_date)
order by dayofweek(appointment_date);
 
# APPOINTMENTS BY HOUR OF DAY (IDENTIFIES PEAK CLINIC HOURS)
select
hour(appointment_time) as appointment_hour,
count(appointment_id) as total_appointments
from appointments
group by hour(appointment_time)
order by appointment_hour;
 
# PATIENTS WITH MORE THAN ONE APPOINTMENT (REPEAT PATIENTS)
select
p.patient_id,
p.first_name,
p.last_name,
count(a.appointment_id) as total_visits
from patients p
join appointments a on p.patient_id = a.patient_id
group by p.patient_id, p.first_name, p.last_name
having count(a.appointment_id) > 1
order by total_visits desc;
 
# REASON FOR VISIT VS APPOINTMENT STATUS (WHICH REASONS SEE THE MOST NO-SHOWS)
select
reason_for_visit,
count(case when status = 'No-show' then 1 end) as no_shows,
count(appointment_id) as total_appointments,
round(count(case when status = 'No-show' then 1 end) * 100.0 / count(appointment_id), 2) as no_show_rate_pct
from appointments
group by reason_for_visit
order by no_show_rate_pct desc;
 
# DOCTOR WORKLOAD COMPARED TO HOSPITAL-WIDE AVERAGE
select
d.doctor_id,
d.first_name,
d.last_name,
count(a.appointment_id) as total_appointments,
(select round(count(*) / count(distinct doctor_id), 1) from appointments) as avg_appointments_per_doctor
from doctors d
left join appointments a on d.doctor_id = a.doctor_id
group by d.doctor_id, d.first_name, d.last_name
order by total_appointments desc;
 
# SECTION 2: REVENUE ANALYSIS
 
# TOTAL REVENUE GENERATED PER HOSPITAL BRANCH
select
d.hospital_branch,
sum(b.amount) as total_revenue,
dense_rank() over (order by sum(b.amount) desc) as ranking
from doctors d
left join appointments a on d.doctor_id = a.doctor_id
left join treatments t on a.appointment_id = t.appointment_id
left join billing b on t.treatment_id = b.treatment_id
group by d.hospital_branch
order by ranking;
 
# DOCTORS RANKED BY REVENUE GENERATED
select
d.doctor_id,
d.first_name,
d.last_name,
sum(b.amount) as total_revenue,
dense_rank() over (order by sum(b.amount) desc) as ranking
from doctors d
left join appointments a on d.doctor_id = a.doctor_id
left join treatments t on a.appointment_id = t.appointment_id
left join billing b on t.treatment_id = b.treatment_id
group by d.doctor_id, d.first_name, d.last_name
order by ranking;
 
# TOTAL REVENUE GENERATED PER MONTH
select
monthname(b.bill_date) as month_name,
month(b.bill_date) as month_number,
sum(b.amount) as total_revenue
from billing b
group by monthname(b.bill_date), month(b.bill_date)
order by month(b.bill_date);
 
# PAYMENT METHOD RANKED BY REVENUE GENERATED
select
b.payment_method,
sum(b.amount) as total_revenue,
dense_rank() over (order by sum(b.amount) desc) as ranking
from billing b
group by b.payment_method
order by ranking;
 
# TOTAL REVENUE GENERATED BY EACH TREATMENT TYPE
select
t.treatment_type,
sum(b.amount) as total_revenue
from treatments t
left join billing b on b.treatment_id = t.treatment_id
group by t.treatment_type
order by total_revenue desc;
 
# INSURANCE PROVIDER RANKED BY TOTAL REVENUE GENERATED
select
p.insurance_provider,
sum(b.amount) as total_revenue,
dense_rank() over (order by sum(b.amount) desc) as ranking
from patients p
left join billing b on p.patient_id = b.patient_id
group by p.insurance_provider
order by ranking;
 
# AVERAGE TREATMENT COST BY TREATMENT TYPE
select
treatment_type,
round(avg(cost), 2) as avg_cost,
count(*) as total_treatments
from treatments
group by treatment_type
order by avg_cost desc;
 
# TOTAL REVENUE BY AGE GROUP

select
case
when timestampdiff(year, p.date_of_birth, curdate()) between 20 and 35 then 'Young Adult (20-35)'
when timestampdiff(year, p.date_of_birth, curdate()) between 36 and 50 then 'Adult (36-50)'
when timestampdiff(year, p.date_of_birth, curdate()) between 51 and 65 then 'Middle Age (51-65)'
when timestampdiff(year, p.date_of_birth, curdate()) between 66 and 80 then 'Senior (66-80)'
else 'Other'
end as age_group,
sum(b.amount) as total_revenue
from patients p
join appointments a on p.patient_id = a.patient_id
join treatments t on a.appointment_id = t.appointment_id
join billing b on t.treatment_id = b.treatment_id
group by age_group
order by total_revenue desc;
 
# AVERAGE REVENUE PER PATIENT

select
round(sum(b.amount) / count(distinct b.patient_id), 2) as avg_revenue_per_patient
from billing b;
 
# AVERAGE REVENUE PER APPOINTMENT

select
round(sum(b.amount) / count(distinct a.appointment_id), 2) as avg_revenue_per_appointment
from appointments a
join treatments t on a.appointment_id = t.appointment_id
join billing b on t.treatment_id = b.treatment_id;
 
# TOP 5 HIGHEST-BILLING PATIENTS

select
p.patient_id,
p.first_name,
p.last_name,
sum(b.amount) as total_billed
from patients p
join billing b on p.patient_id = b.patient_id
group by p.patient_id, p.first_name, p.last_name
order by total_billed desc
limit 5;
 
# REVENUE BY HOSPITAL BRANCH AND PAYMENT METHOD COMBINED

select
d.hospital_branch,
b.payment_method,
sum(b.amount) as total_revenue
from doctors d
join appointments a on d.doctor_id = a.doctor_id
join treatments t on a.appointment_id = t.appointment_id
join billing b on t.treatment_id = b.treatment_id
group by d.hospital_branch, b.payment_method
order by d.hospital_branch, total_revenue desc;
 

 

 



