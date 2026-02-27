-- 1. Hires by Technology 
SELECT 
    t.Technology_Name AS Technology, 
    COUNT(f.Application_SK) AS Total_Hires
FROM Fact_Applications f
JOIN Dim_Technology t ON f.Technology_SK = t.Technology_SK
WHERE f.Is_Hired = 1
GROUP BY t.Technology_Name
ORDER BY Total_Hires DESC;


-- 2. Hires by Year 
SELECT 
    d.Year AS Application_Year, 
    COUNT(f.Application_SK) AS Total_Hires
FROM Fact_Applications f
JOIN Dim_Date d ON f.Date_SK = d.Date_SK
WHERE f.Is_Hired = 1
GROUP BY d.Year
ORDER BY d.Year ASC;

-- 3. Hires by Seniority 
SELECT 
    c.Seniority, 
    COUNT(f.Application_SK) AS Total_Hires
FROM Fact_Applications f
JOIN Dim_Candidate c ON f.Candidate_SK = c.Candidate_SK
WHERE f.Is_Hired = 1
GROUP BY c.Seniority
ORDER BY Total_Hires DESC;

-- 4. Hires by Country (United States of America, Brazil, Colombia, and Ecuador)
SELECT 
    l.Country, 
    COUNT(f.Application_SK) AS Total_Hires
FROM Fact_Applications f
JOIN Dim_Location l ON f.Location_SK = l.Location_SK
WHERE f.Is_Hired = 1 
  AND l.Country IN ('United States of America', 'Brazil', 'Colombia', 'Ecuador')
GROUP BY l.Country
ORDER BY Total_Hires DESC;

-- 5. Hiring Rate by Technology
SELECT 
    t.Technology_Name AS Technology,
    COUNT(f.Application_SK) AS Total_Applicants,
    SUM(f.Is_Hired) AS Total_Hires,
    ROUND((SUM(f.Is_Hired) / COUNT(f.Application_SK)) * 100, 2) AS Conversion_Rate_Pct
FROM Fact_Applications f
JOIN Dim_Technology t ON f.Technology_SK = t.Technology_SK
GROUP BY t.Technology_Name
ORDER BY Conversion_Rate_Pct DESC;

-- 6. Average Scores by Seniority Level
SELECT 
    c.Seniority,
    ROUND(AVG(f.Code_Challenge_Score), 2) AS Avg_Code_Score,
    ROUND(AVG(f.Technical_Interview_Score), 2) AS Avg_Interview_Score
FROM Fact_Applications f
JOIN Dim_Candidate c ON f.Candidate_SK = c.Candidate_SK
GROUP BY c.Seniority
ORDER BY Avg_Code_Score DESC;