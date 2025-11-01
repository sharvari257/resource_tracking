# Resource Tracking System

## DESCRIPTION
This project is a small-scale system monitoring tool that tracks CPU usage using
Python’s psutil library, stores it in a MySQL database, and visualizes it on a real-time dashboard built using Dash and Plotly. It helps us understand how to combine backend data collection, storage, and frontend visualization — all in Python.

## DIRECTORY STRUCTURE
resource_tracking/
├── cpu_usage_alert.py
├── dash_app.py
├── graph_data.py
├── notes.txt
├── task.py
├── task2.py
├── temp-plot.html
├── testing.py
└── __pycache__/
└── email.cpython-312.pyc

## OVERVIEW
Language    Python
DB          MySQL
Libs        psutil, mysql.connector, dash, plotly, pandas, smtplib, email
Dashboard   Dash (a python web framework for interactive dashboards)

## FEATURES
- 📊 **Real-time CPU usage tracking**
- ⚠️ **Automatic alerting** when CPU crosses a threshold
- 📈 **Interactive dashboard** built with Dash (Plotly)
- 🧠 **Background tasks** to log and process system data
- 🧩 **Modular code structure** — easy to extend and learn from

## INSTALLATION and SETUP
bash
git clone https://github.com/sharvari257/resource-tracking-system.git
cd resource_tracking

create virtual environment
python -m venv venv
source venv/bin/activate      # (Mac/Linux)
venv\Scripts\activate         # (Windows)

To install the required libraries, run:
```
pip install -r requirements.txt
```

## HOW IT WORKS
1. cpu_usage_alert.py continuously checks CPU metrics.
2. When a threshold is crossed, it triggers a warning or logs the event.
3. graph_data.py formats collected data for display.
4. dash_app.py renders a dashboard (via Dash/Plotly) that updates in real-time.
5. Background scripts (task.py, task2.py) handle logging or periodic updates.

## EXAMPLE OUTPUT
CPU Usage Alert Example:
```Warning! CPU usage exceeded 85% at 12:45:20```

Dashboard Example:
* Displays CPU usage graph updating in real-time
* Highlights alert regions or spikes visually

## CONTRIBUTING
1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request.

## AUTHOR
**Sharvari Phatkar**
Technical Consultant Engineering Apprentice @ Splunk AppDynamics - Cisco [Now full time]
🎓 B.E. in Computer Technology | PG-Diploma in Cloud Technology
💡 Interests: Linux, Cloud, Containers, Monitoring, and DevOps Tools


## Acknowledgments
- [Plotly](https://plotly.com/) for data visualization.
- [Dash](https://dash.plotly.com/) for the web dashboard.
