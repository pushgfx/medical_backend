CREATE TABLE roles (
	role_id int NOT NULL AUTO_INCREMENT,
	role_name varchar(40) NOT NULL,
	PRIMARY KEY (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE users (
	id int NOT NULL AUTO_INCREMENT,
	username varchar(120) NOT NULL,
	password varchar(128) NOT NULL,
	role_id int NOT NULL,
	user_role_id int NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE specializations (
	specialist_id int NOT NULL AUTO_INCREMENT,
	specialization_name varchar(120) NOT NULL,
	PRIMARY KEY (specialist_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE doctors (
	doctor_id int NOT NULL AUTO_INCREMENT,
	first_name varchar(80) NOT NULL,
	middle_initial varchar(1) NOT NULL,
	last_name varchar(80) NOT NULL,
	phone int(11) NOT NULL,
	specialist_id int NOT NULL,
	PRIMARY KEY (doctor_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE offices (
	office_id int NOT NULL AUTO_INCREMENT,
	office_name varchar(100) NOT NULL,
	street_1 varchar(120) NOT NULL,
	city varchar(40) NOT NULL,
	state varchar(2) NOT NULL,
	zipcode int(9) NOT NULL,
	phone varchar(20) NOT NULL,
	PRIMARY KEY (office_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE doctor_office_affiliations (
	id int NOT NULL AUTO_INCREMENT,
	doctor_id int NOT NULL,
	office_id int NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE doctor_office_availability (
	id int NOT NULL AUTO_INCREMENT,
	doctor_id int NOT NULL,
	office_id int NOT NULL,
	day_of_week varchar(3) NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	is_available varchar(1) NOT NULL,
	reason_for_unavailability varchar(500),
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE clients (
	client_id int NOT NULL AUTO_INCREMENT,
	first_name varchar(80) NOT NULL,
	middle_initial varchar(1) NOT NULL,
	last_name varchar(80) NOT NULL,
	street_1 varchar(120) NOT NULL,
	city varchar(40) NOT NULL,
	state varchar(2) NOT NULL,
	zipcode int(9) NOT NULL,
	phone varchar(20) NOT NULL,
	date_of_birth date NOT NULL,
	gender varchar(1) NOT NULL,
	marital_status varchar(1) NOT NULL,
	race varchar(20) NOT NULL,
	email varchar(100) NOT NULL,
	primary_doctor int,
	PRIMARY KEY (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE client_doctor_affiliation (
	id int NOT NULL AUTO_INCREMENT,
	client_id int NOT NULL,
	doctor_id int NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE medications (
	medication_id int NOT NULL AUTO_INCREMENT,
	medication_name varchar(120) NOT NULL,
	PRIMARY KEY (medication_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE medication_forms (
	form_id int NOT NULL AUTO_INCREMENT,
	form_name varchar(120) NOT NULL,
	PRIMARY KEY (form_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE prescribed_medications (
	id int NOT NULL AUTO_INCREMENT,
	appt_id int NOT NULL,
	client_id int NOT NULL,
	medication_id int NOT NULL,
	form_id int NOT NULL,
	dosage varchar(120) NOT NULL,
	indication varchar(120) NOT NULL,
	date_prescribed DATETIME NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE appointments (
    appt_id int NOT NULL AUTO_INCREMENT,
    client_id int NOT NULL,
    office_id int NOT NULL,
    doctor_id int NOT NULL,
    was_referred int(1) NOT NULL,
    referring_doctor_id int,
    appt_start_time DATETIME NOT NULL,
    estimated_end_time DATETIME NOT NULL,
    appt_status varchar(20) NOT NULL,
    booking_date DATETIME NOT NULL,
    booking_method varchar(20) NOT NULL,
    PRIMARY KEY (appt_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE appointments_meta_data (
	appt_id int NOT NULL,
	client_id int NOT NULL,
	height int NOT NULL,
	weight int NOT NULL,
	blood_pressure varchar(7) NOT NULL,
	reason_for_visit varchar(500) NOT NULL,
	blood_testing int(1) NOT NULL,
	blood_test_results varchar(500),
	additional_testing int(1) NOT NULL,
	additional_test_results varchar(500),
	treatment varchar(500) NOT NULL,
	new_prescriptions int(1) NOT NULL,
	patient_notes varchar(500),
	actual_end_time DATETIME NOT NULL
    -- primary key is also a foreign key. I don't think so
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE users ADD FOREIGN KEY (role_id) REFERENCES roles(role_id) ;
ALTER TABLE clients ADD FOREIGN KEY (primary_doctor) REFERENCES doctors(doctor_id) ;
ALTER TABLE doctors ADD FOREIGN KEY (specialist_id) REFERENCES specializations(specialist_id) ;
ALTER TABLE doctor_office_affiliations ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ;
ALTER TABLE doctor_office_affiliations ADD FOREIGN KEY (office_id) REFERENCES offices(office_id) ;
ALTER TABLE appointments ADD FOREIGN KEY (client_id) REFERENCES clients(client_id) ;
ALTER TABLE appointments ADD FOREIGN KEY (office_id) REFERENCES offices(office_id) ;
ALTER TABLE prescribed_medications ADD FOREIGN KEY (medication_id) REFERENCES medications(medication_id) ;
ALTER TABLE prescribed_medications ADD FOREIGN KEY (form_id) REFERENCES medication_forms(form_id) ;
ALTER TABLE appointments_meta_data ADD FOREIGN KEY (appt_id) REFERENCES appointments(appt_id);
ALTER TABLE appointments_meta_data ADD FOREIGN KEY (client_id) REFERENCES clients(client_id);
ALTER TABLE prescribed_medications ADD FOREIGN KEY (appt_id) REFERENCES appointments(appt_id);
ALTER TABLE client_doctor_affiliation ADD FOREIGN KEY (client_id) REFERENCES clients(client_id);
ALTER TABLE client_doctor_affiliation ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);
