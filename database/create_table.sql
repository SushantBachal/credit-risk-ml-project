CREATE DATABASE IF NOT EXISTS CreditCardDB;

USE CreditCardDB;

CREATE TABLE IF NOT EXISTS Credit_Card_info(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    SeriousDlqin2yrs INT,
    RevolvingUtilizationOfUnsecuredLines FLOAT,
    age INT,
    `NumberOfTime30-59DaysPastDueNotWorse` INT,
    DebtRatio FLOAT,
    MonthlyIncome FLOAT NULL,
    NumberOfOpenCreditLinesAndLoans INT,
    NumberOfTimes90DaysLate INT,
    NumberRealEstateLoansOrLines INT,
    `NumberOfTime60-89DaysPastDueNotWorse` INT,
    NumberOfDependents FLOAT NULL
)



