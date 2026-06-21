USE creditcarddb;

-- EDA Queries

-- THE TOTAL NUMBER OF ROWS IN THE CREDIT_CARD_INFO TABLE IS 150,000
SELECT COUNT(*) AS Total_raws
FROM credit_card_info;

-- THE NULL VALUES IN THE MONTHLY INCOME COLUMN IS 31,365
SELECT COUNT(MonthlyIncome) AS Total_nullvalues_in_MonthlyIncome
FROM credit_card_info
WHERE MonthlyIncome = "NULL"

-- THE NULL VALUES IN THE NUMBER OF DEPENDENTS COLUMN IS 90,8026
SELECT COUNT(NumberOfDependents) AS Total_nullvalues_in_NumberOfDependents
FROM credit_card_info
WHERE NumberOfDependents = "NULL"

-- Class Imbalance Finding: 10,026 defaulted (6.7%) vs 139,974 not defaulted (93.3%)
-- Dataset is heavily imbalanced -- SMOTE required during model training
SELECT COUNT(SeriousDlqin2yrs) 
FROM credit_card_info
WHERE SeriousDlqin2yrs = 1;

-- AGE ANALYSIS: 1 (0.01%) of customers are under 18 years old, and 13 (0.02%) are over 100 years old
SELECT COUNT(age)
FROM credit_card_info
WHERE age < 18

-- AGE ANALYSIS: 13 (O.02%) of customers are over 100 years old 
SELECT COUNT(age)
FROM credit_card_info
WHERE age > 100;


SELECT MIN(age) AS Minimum_age,
MAX(age) AS Maximum_age,
AVg(age) AS Average_age
FROM credit_card_info


-- MonthlyIncome Stats: Min=0 (suspicious), Max=3,008,750 (extreme outlier), Avg=5,348
-- Min=0 likely caused by text "NULL" values or bad data -- investigate in notebook
-- Max=3,008,750 is an extreme outlier -- needs treatment in preprocessing
SELECT MIN(MonthlyIncome) AS Minimum_MonthlyIncome,
MAX(MonthlyIncome) AS Maximum_MonthlyIncome,
AVg(MonthlyIncome) AS Average_MonthlyIncome
FROM credit_card_info


SELECT MIN(DebtRatio) AS Minimum_DebtRatio,
MAX(DebtRatio) AS Maximum_DebtRatio,
AVg(DebtRatio) AS Average_DebtRatio
FROM credit_card_info


-- DebtRatio Outlier Finding: 35,137 rows (23%) have DebtRatio > 1
-- Extreme values like 300,000+ exist -- needs capping or removal in preprocessing
SELECT COUNT(DebtRatio) AS Total_DebtRatio_Values
FROM credit_card_info
WHERE DebtRatio > 1;


-- Suspicious Values Finding: All three late payment columns have exactly 269 rows with 96/98
-- Same 269 rows affected across all columns -- entire rows are bad data
-- Action: remove these 269 rows entirely during preprocessing
SELECT 
    COUNT(CASE WHEN NumberOfTimes90DaysLate IN (96,98) THEN 1 END) AS Total_90DaysLate,
    COUNT(CASE WHEN `NumberOfTime60-89DaysPastDueNotWorse` IN (96,98) THEN 1 END) AS Total_60_89DaysLate,
    COUNT(CASE WHEN `NumberOfTime30-59DaysPastDueNotWorse` IN (96,98) THEN 1 END) AS Total_30_59DaysLate
FROM credit_card_info;


-- RevolvingUtilization Outlier: 3,321 rows have values above 1
-- Should be capped at 1 during preprocessing as it is a percentage column
SELECT COUNT(RevolvingUtilizationOfUnsecuredLines) AS Total_RevolvingUtilizationOfUnsecuredLines_Values
FROM credit_card_info
WHERE RevolvingUtilizationOfUnsecuredLines > 1;
