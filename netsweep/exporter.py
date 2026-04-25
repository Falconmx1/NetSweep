import json
import csv
from jinja2 import Template
import pdfkit

class Exporter:
    @staticmethod
    def export(data, filename, format):
        if format == "json":
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
        elif format == "csv":
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["IP", "Status"])
                for host in data.get("hosts", []):
                    writer.writerow([host["ip"], host["status"]])
        elif format == "html":
            template = Template("<html><body><pre>{{ data }}</pre></body></html>")
            with open(filename, "w") as f:
                f.write(template.render(data=data))
        elif format == "pdf":
            pdfkit.from_string(str(data), filename)
