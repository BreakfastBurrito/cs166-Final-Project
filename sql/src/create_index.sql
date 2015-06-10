/* ---------------------------------------- */
/* Kenley Arai                              */
/* Antoine Guerrero                         */
/* Group 20                                 */
/* ---------------------------------------- */

CREATE UNIQUE INDEX USR_INDEX ON USR(userId);
CREATE INDEX NAME_INDEX ON USR(name);
CREATE INDEX WORK_EXPR_INDEX ON WORK_EXPR(userId, company, role, startDate, location, startDate, endDate);
CREATE INDEX EDUCATIONAL_DETAILS_INDEX ON EDUCATIONAL_DETAILS(userId, institutionName, major, degree, startDate, endDate);
CREATE INDEX MESSAGE_INDEX on MESSAGE(msgId);
CREATE INDEX SENDER_MESSAGE_INDEX on MESSAGE(senderId, status);
CREATE INDEX RECEIVER_MESSAGE_INDEX on MESSAGE(receiverId, status);
CREATE INDEX CONNECTION_USR_INDEX on CONNECTION_USR(userId, connectionId);
