CREATE TABLE bookings
(
	idBooking INT AUTO_INCREMENT,
    idProperty INT NOT NULL,
    initDate DATETIME NOT NULL,
    endDate DATETIME NOT NULL,
    total DOUBLE NOT NULL,
	dni VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    CONSTRAINT pk_bookings_idBooking PRIMARY KEY(idBooking),
    CONSTRAINT fk_bookings_idProperty FOREIGN KEY(idProperty) REFERENCES properties(idProperty) ON UPDATE CASCADE,
    CONSTRAINT chk_bookings_initDate_endDate CHECK(initDate<=endDate)
);