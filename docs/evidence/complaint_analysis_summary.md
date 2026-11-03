# Complaint Analysis Summary

## 1. Overview

This report provides a descriptive analysis of the complaint data contained in complaints.csv.
The analysis was performed using Python and pandas as part of Exercise 2.4.1.
Total complaints analyzed: 120
The objective is to identify complaint distribution patterns, the highest-volume category, and average resolution times for closed complaints.

## 2. Complaint Distribution

### 2.1 Complaints by Category

| Category | Count | Percentage (%) |
|---|---:|---:|
| Mortgage Servicing | 31 | 25.8 |
| Card or Transaction Dispute | 25 | 20.8 |
| Service Quality | 21 | 17.5 |
| Digital Banking | 19 | 15.8 |
| Fees | 15 | 12.5 |
| Account Access | 9 | 7.5 |

Mortgage Servicing is the highest-volume complaint category, with 31 complaints representing 25.8% of all complaints.

### 2.2 Complaints by Status

| Status | Count | Percentage (%) |
|---|---:|---:|
| Closed | 34 | 28.3 |
| In Review | 32 | 26.7 |
| Escalated | 30 | 25.0 |
| Open | 24 | 20.0 |

**Key observation:** Of the 120 complaints, 34 are closed (28.3%), while 86 (71.7%) have a status other than Closed.

## 3. Resolution Performance

Average resolution time was calculated for closed complaints only, grouped by category.

| Category | Average Resolution Time (days) |
|---|---:|
| Account Access | 16 |
| Card or Transaction Dispute | 11 |
| Digital Banking | 8 |
| Fees | 10 |
| Mortgage Servicing | 9 |
| Service Quality | 6 |

Key observations:
- Account Access has the highest observed average resolution time at 16 days.
- Service Quality has the lowest observed average resolution time at 6 days.
- These figures describe the closed complaints in the analyzed dataset and should not be interpreted as evidence of changes in performance over time.

## 4. Metric Definitions

Total Complaints: Number of complaint records included in the dataset.
Complaint Count by Category: Number of complaints belonging to each category.
Complaint Count by Status: Number of complaints associated with each status.
Complaint Percentage: Number of complaints in a given group divided by the total number of complaints, multiplied by 100.
Highest-Volume Category: Category containing the greatest number of complaints. Categories with equal maximum counts are considered tied.
Resolution Time: Difference, in days, between the complaint resolution date and creation date.
Average Resolution Time: Arithmetic mean of valid resolution durations for closed complaints within each category, rounded to the nearest whole day.

## 5. Data Quality and Limitations

- The dataset contains 120 complaint records.
- No missing values were reported for complaint identifiers, customer identifiers, category, status, or creation date.
- The resolution date is missing for 86 complaints.
- The number of missing resolution dates matches the number of complaints not marked as Closed. This does not independently establish that they refer to exactly the same records.
- Resolution metrics are calculated only for closed complaints with valid date values.
- Results are based exclusively on the provided synthetic dataset.

## 6. Conclusion

Mortgage Servicing represents the largest share of complaints (25.8%). Most complaint records (71.7%) are not marked as Closed.
Among closed complaints, average resolution durations vary by category, ranging from 6 days for Service Quality to 16 days for Account Access.