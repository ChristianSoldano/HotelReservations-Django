CREATE TABLE accounts
(
	idAccount INT AUTO_INCREMENT,
    accountType ENUM('administrator','host'),
    dni VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(1000) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    phoneNumber VARCHAR(100) NOT NULL,
    CONSTRAINT pk_accounts_idAccount PRIMARY KEY(idAccount),
    CONSTRAINT uk_accounts_dni UNIQUE(dni),
    CONSTRAINT uk_accounts_email UNIQUE(email),
	CONSTRAINT uk_accounts_phoneNumber UNIQUE(phoneNumber)
);