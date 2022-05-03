from router import MultiApp
from pages import create_report, show_reports

app = MultiApp()

# Add all your application here
app.add_app("Create Report", create_report.app)
app.add_app("Show Report", show_reports.app)

# The main app
app.run()
