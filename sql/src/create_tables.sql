/* ---------------------------------------- */
/* Kenley Arai                              */
/* Antoine Guerrero                         */
/* Group 20                                 */
/* ---------------------------------------- */

DROP TABLE WORK_EXPR;
DROP TABLE EDUCATIONAL_DETAILS;
DROP TABLE MESSAGE;
DROP TABLE CONNECTION_USR;
DROP TABLE USR;
SET datestyle TO "postgres, MDY";
CREATE TABLE USR(
	userId varchar(32) UNIQUE NOT NULL,
	password varchar(32) NOT NULL,
	email text NOT NULL,
	name char(50),
	dateOfBirth date,
	Primary Key(userId));

CREATE TABLE WORK_EXPR(
	userId char(32) NOT NULL,
	company char(50) NOT NULL,
	role char(50) NOT NULL,
	location char(50),
	startDate date,
	endDate date,
	PRIMARY KEY(userId,company,role,startDate));

CREATE TABLE EDUCATIONAL_DETAILS(
	userId char(32) NOT NULL,
	institutionName char(50) NOT NULL,
	major char(50) NOT NULL,
	degree char(50) NOT NULL,
	startdate date,
	enddate date,
	PRIMARY KEY(userId,major,degree));

CREATE TABLE MESSAGE(
	msgId integer UNIQUE NOT NULL,
	senderId char(32) NOT NULL,
	receiverId char(32) NOT NULL,
	contents TEXT NOT NULL,
	sendTime timestamp,
	deleteStatus integer,
	status char(30) NOT NULL,
	PRIMARY KEY(msgId));

CREATE TABLE CONNECTION_USR(
	userId char(32) NOT NULL,
	connectionId char(32) NOT NULL,
	status char(30) NOT NULL,
	PRIMARY KEY(userId,connectionId));

COPY USR(
  userId,
  password,
  email,
  name,
  dateOfBirth)
FROM '/home/antoine/cs166-Final-Project/data/usr.csv'
WITH DELIMITER ',';

COPY  WORK_EXPR(
	userId,
	company,
	role,
	location,
	startDate,
	endDate)
FROM '/home/antoine/cs166-Final-Project/data/work_ex.csv'
WITH DELIMITER ',';

COPY EDUCATIONAL_DETAILS(
  userId,
  institutionName,
  major,
  degree,
  startdate,
  enddate)
FROM '/home/antoine/cs166-Final-Project/data/edu_det.csv'
WITH DELIMITER ',';

COPY MESSAGE(
  msgId,
  senderId,
  receiverId,
  contents,
  sendTime,
  deleteStatus,
  status)
FROM '/home/antoine/cs166-Final-Project/data/message.tsv';

COPY CONNECTION_USR(
  userId,
  connectionId,
  status)
FROM '/home/antoine/cs166-Final-Project/data/connection.csv'
WITH DELIMITER ',';
