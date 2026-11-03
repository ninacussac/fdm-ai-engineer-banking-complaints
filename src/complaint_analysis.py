import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "complaints.csv"
REQUIRED_COLUMNS = ['complaint_id', 'customer_id', 'category','status','created_date','resolved_date']

OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "complaint_analysis_output.csv"

def load_complaint(file_path):
    try:
        complaint_data = pd.read_csv(file_path)
        if complaint_data.empty:
            print("Warning: The CSV file contains no records.")
            return None

        print(f"File loaded successfully: {len(complaint_data)} records.")
        return complaint_data
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return None


    
def validate_complaints(df):
    # Check if all required columns are present in the DataFrame
    missing_columns=[]
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Report missing-value counts
    print("Missing-value counts:")
    for column in REQUIRED_COLUMNS:
        missing_count = df[column].isna().sum()
        print(f"{column}: {missing_count} missing values")


def calculate_complaint_distribution(df, column_name):
    # Calculate counts and percentages for the selected column
    counts = df[column_name].value_counts()
    nb_complaints = len(df)
    percentages = round(counts/nb_complaints * 100, 1)

    # Create a DataFrame to display counts and percentages
    result = pd.DataFrame({
        "Count": counts,
        "Percentage (%)": percentages
    })  
    result = result.reset_index()  
    return result


def calculate_average_resolution_time(df):

    df_closed = df[df['status'] == 'Closed'].copy()
    print(f"Number of closed complaints: {len(df_closed)}")

    df_closed['created_date'] = pd.to_datetime(df_closed['created_date'], errors='coerce')
    df_closed['resolved_date'] = pd.to_datetime(df_closed['resolved_date'], errors='coerce')

    missing_resolution = df_closed["resolved_date"].isna()

    if missing_resolution.any():
        print(
            f"Warning: {missing_resolution.sum()} closed complaint(s) "
            "have no resolution date and will be excluded from "
            "the average resolution time calculation."
        )

    df_closed['resolution_time'] = (df_closed['resolved_date'] - df_closed['created_date']).dt.days

    grouped = df_closed.groupby('category')

    avg_resolution_time = (
        grouped['resolution_time']
        .mean()
        .round(0)
        .astype('Int64')
        .reset_index()
        .rename(columns={'resolution_time': 'avg_resolution_time_days'})
        )

    return avg_resolution_time


def export_results_to_csv(
    total_complaints,
    category_summary,
    status_summary,
    resolution_summary,
    output_path
):
    rows = []
    # Total number of complaints
    rows.append({
        "metric": "total_complaints",
        "group": "All",
        "value": total_complaints,
        "unit": "complaints"
    })

    for _, row in category_summary.iterrows():
        rows.append({
            "metric": "category_count",
            "group": row["category"],
            "value": row["Count"],
            "unit": "complaints"
        })

        rows.append({
            "metric": "category_percentage",
            "group": row["category"],
            "value": row["Percentage (%)"],
            "unit": "%"
        })

    for _, row in status_summary.iterrows():
        rows.append({
            "metric": "status_count",
            "group": row["status"],
            "value": row["Count"],
            "unit": "complaints"
        })

        rows.append({
            "metric": "status_percentage",
            "group": row["status"],
            "value": row["Percentage (%)"],
            "unit": "%"
        })

    # Average resolution times
    for _, row in resolution_summary.iterrows():
        rows.append({
            "metric": "avg_resolution_time",
            "group": row["category"],
            "value": row["avg_resolution_time_days"],
            "unit": "days"
        })

    # Create a DataFrame and export
    output_df = pd.DataFrame(
        rows,
        columns=["metric", "group", "value", "unit"]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)

    print(f"\nCSV exported successfully to: {output_path}")


    

def main():

    complaint_data = load_complaint(CSV_PATH)

    if complaint_data is None:
        return

    if("date_opened" not in complaint_data.columns or "date_closed" not in complaint_data.columns):
        raise ValueError("Missing required columns: 'date_opened' and/or 'date_closed'")

    complaint_data["created_date"] = complaint_data["date_opened"]
    complaint_data["resolved_date"] = complaint_data["date_closed"]

    validate_complaints(complaint_data)

    total_complaints = len(complaint_data)
    print(f"Total complaints: {total_complaints}")

    print("\nNumber of complaints per category:")
    category_summary = calculate_complaint_distribution(complaint_data, "category")
    print(category_summary)

    if not category_summary.empty:
        valid_categories = category_summary.dropna(subset=['category'])
        if not valid_categories.empty:
            # Find the highest complaint count
            max_count = valid_categories['Count'].max()
            # Select all categories with this count
            highest_volume = valid_categories[valid_categories['Count'] == max_count]
            print("\nHighest-volume categories:")
            print(highest_volume)

    print("\nNumber of complaints per status:")
    status_summary = calculate_complaint_distribution(complaint_data, "status")
    print(status_summary)

    print("\nAverage resolution time per category:")
    avg_resolution_summary = calculate_average_resolution_time(complaint_data)
    print(avg_resolution_summary)


    export_results_to_csv(
        total_complaints,
        category_summary,
        status_summary,
        avg_resolution_summary,
        OUTPUT_CSV
    )

if __name__ == "__main__":
    main()
