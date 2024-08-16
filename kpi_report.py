import pandas as pd


def generate_kpi_report(input_file='network_status.csv', output_file='network_kpi_report.csv'):
    """
    Generate KPI report from network status data.
    """
    df = pd.read_csv(input_file)

    # Calculate KPIs
    total_devices = df['Device'].nunique()
    uptime = df[df['Status'] == 'Up'].groupby('Device').size()
    downtime = df[df['Status'] == 'Down'].groupby('Device').size()

    # Creating the KPI DataFrame
    kpi_data = {
        'Device': df['Device'].unique(),
        'Total Checks': uptime.add(downtime, fill_value=0),
        'Uptime': uptime,
        'Downtime': downtime
    }

    kpi_df = pd.DataFrame(kpi_data).fillna(0)
    kpi_df['Uptime Percentage'] = (kpi_df['Uptime'] / kpi_df['Total Checks']) * 100
    kpi_df['Downtime Percentage'] = (kpi_df['Downtime'] / kpi_df['Total Checks']) * 100

    # Save the KPI report to a CSV file
    kpi_df.to_csv(output_file, index=False)
    print(f"KPI report saved to {output_file}")


# Main execution
if __name__ == "__main__":
    generate_kpi_report()
