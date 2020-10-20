CREATE TABLE booking_periods
(
	idBookingPeriod INT AUTO_INCREMENT,
    idProperty INT NOT NULL,
	initDate DATETIME NOT NULL,
    endDate DATETIME NOT NULL,
    CONSTRAINT pk_booking_periods_idBookingPeriod PRIMARY KEY(idBookingPeriod),
    CONSTRAINT fk_booking_periods_idProperty FOREIGN KEY(idProperty) REFERENCES properties(idProperty) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_booking_periods_initDate_endDate CHECK(initDate<=endDate)
);