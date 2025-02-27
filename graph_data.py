import psutil
import mysql.connector
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import plotly.graph_objects as go

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pass123',
    auth_plugin='mysql_native_password'
)

# Create a cursor object for SQL queries
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS python_db;")
cur.execute("USE python_db;")
cur.execute("CREATE TABLE IF NOT EXISTS usage_tbl(ID int AUTO_INCREMENT PRIMARY KEY, col_dateTime DATETIME DEFAULT CURRENT_TIMESTAMP, min_usage INT, max_usage INT, avg_usage FLOAT);")

# Email configuration
admin_email = "test107.dummy@gmail.com"
admin_password = "bpry flby krlk qdya"  # app password
recipient_email = "sphatkar@cisco.com"

# Function to send email notification
def send_email_notification(cpu_usage):
    msg = MIMEMultipart()
    subject = "CPU usage notification"
    body = f"Average CPU usage: {cpu_usage}% at {time.ctime()} Kindly take action!"
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = admin_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # for secure smtp connection
        server.login(admin_email, admin_password)
        server.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Failed to send email")
        print(e)
    finally:
        server.quit()  # close smtp server

# Function to send report email
def report(body):
    msg = MIMEMultipart()
    subject = f"{time.ctime()} CPU usage report"
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = admin_email
    msg['To'] = recipient_email
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # for secure smtp connection
        server.login(admin_email, admin_password)
        server.sendmail(admin_email, recipient_email, msg.as_string())  # Send the message
        print("Report email sent!")
    except Exception as e:
        print("Failed to send report email")
        print(e)
    finally:
        server.quit()  # close smtp server

# Function to get SQL data
def get_tbl_data(start_date=None, end_date=None):
    # Query to select all data from usage_tbl
    cur.execute("SELECT * FROM usage_tbl;")
    rows = cur.fetchall()  # Fetch all rows from the query result

    # Create a string to hold the table data
    table_data = "ID\tDate Time\tMin Usage\tMax Usage\tAvg Usage\n"
    table_data += "-" * 60 + "\n"  # Add a separator line

    # Format each row and append to the table_data string
    for row in rows:
        table_data += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]:.2f}\n"

    return table_data

# Function to create graph
def create_graph():
    cur.execute("SELECT col_dateTime, avg_usage FROM usage_tbl;")
    # cur.execute("SELECT col_dateTime, max_usage FROM usage_tbl;")
    rows = cur.fetchall()
    # extracting first element [timestamp] of each tuple --> store to x
    x = [row[0] for row in rows]
    # extracting second element [avg_usage] of each tuple --> store to y
    y = [row[1] for row in rows]

    fig = go.Figure(data=[
        go.Scatter(x=x, y=y)
    ])

    # Giving axis names and title
    fig.update_layout(title="CPU Usage", xaxis_title="Date Time", yaxis_title="Average Usage")

    fig.show()

create_graph()

# Main execution block
if __name__ == "__main__":
    start_time = time.time()  # start time of the script
    duration = 60  # duration set to 60 seconds [1 min]
    threshold = 5  # Setting threshold value
    cpu_usages = []  # List to store CPU usage readings for the minute

    report_duration = time.time() + 300 #5mins


    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_usages.append(cpu_usage)

            if cpu_usage > threshold:
                print("High CPU usage: ", cpu_usage)

            else:
                print("Normal CPU Usage: ", cpu_usage)

            time.sleep(9)  # Sleep for 9 seconds to make the total interval 10 seconds

            # Check if 1 min time limit is reached
            if time.time() - start_time > duration:
                print("----------------------------")
                # Calculate min, max, and average CPU usage
                min_usage = min(cpu_usages)
                max_usage = max(cpu_usages)
                avg_usage = sum(cpu_usages) / len(cpu_usages)

                if avg_usage > threshold:
                    send_email_notification(avg_usage)  # Send email notification for average usage

                # Insert into table
                cur.execute(f"INSERT INTO usage_tbl(min_usage, max_usage, avg_usage) VALUES({min_usage}, {max_usage}, {avg_usage});")
                conn.commit()

                # Reset the cpu_usage list and start timer for next minute
                cpu_usages.clear()
                start_time = time.time()  # reset time
            if time.time() - report_duration > 0:
                if cpu_usages:  # Ensure cpu_usages is not empty
                    print("Report generated")

                    # Create a string representation of the complete data
                    usage_data = "\n".join(f"Usage {i+1}: {usage}%" for i, usage in enumerate(cpu_usages))

                    report_body = get_tbl_data() + "\n" + usage_data
                    
                    report(report_body)  # Send daily report
                    cpu_usages.clear()  # Reset daily usage list
                    report_duration = time.time() + 300  # Reset report duration for the next report
 

    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        cur.close()  # Close the cursor
        conn.close()  # Close the database connection