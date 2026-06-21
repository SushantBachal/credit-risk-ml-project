USE creditcarddb;

CREATE TABLE stagging_table(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    SeriousDlqin2yrs INT NULL,
    RevolvingUtilizationOfUnsecuredLines FLOAT NULL,
    age INT,
    `NumberOfTime30-59DaysPastDueNotWorse` INT NULL,
    DebtRatio FLOAT NULL,
    MonthlyIncome FLOAT NULL,
    NumberOfOpenCreditLinesAndLoans INT NULL,
    NumberOfTimes90DaysLate INT NULL,
    NumberRealEstateLoansOrLines INT NULL,
    `NumberOfTime60-89DaysPastDueNotWorse` INT NULL,
    NumberOfDependents FLOAT NULL
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cs-training.csv'
IGNORE
INTO TABLE stagging_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(@dummy, SeriousDlqin2yrs, RevolvingUtilizationOfUnsecuredLines, age,
`NumberOfTime30-59DaysPastDueNotWorse`, DebtRatio, MonthlyIncome, NumberOfOpenCreditLinesAndLoans,
NumberOfTimes90DaysLate, NumberRealEstateLoansOrLines, `NumberOfTime60-89DaysPastDueNotWorse`,
NumberOfDependents);

INSERT INTO Credit_Card_info (
    SeriousDlqin2yrs,
    RevolvingUtilizationOfUnsecuredLines,
    age,
    `NumberOfTime30-59DaysPastDueNotWorse`,
    DebtRatio,
    MonthlyIncome,
    NumberOfOpenCreditLinesAndLoans,
    NumberOfTimes90DaysLate,
    NumberRealEstateLoansOrLines,
    `NumberOfTime60-89DaysPastDueNotWorse`,
    NumberOfDependents
)
SELECT
    SeriousDlqin2yrs,
    RevolvingUtilizationOfUnsecuredLines,
    age,
    `NumberOfTime30-59DaysPastDueNotWorse`,
    DebtRatio,
    MonthlyIncome,
    NumberOfOpenCreditLinesAndLoans,
    NumberOfTimes90DaysLate,
    NumberRealEstateLoansOrLines,
    `NumberOfTime60-89DaysPastDueNotWorse`,
    NumberOfDependents
FROM stagging_table;


