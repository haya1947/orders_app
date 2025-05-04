from flask import Flask, render_template_string
import pyodbc
from datetime import datetime, timedelta

app = Flask(__name__)

# פרטי חיבור ל-SQL Server
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=10.10.10.101;"
    "Database=data;"
    "UID=sa;"
    "PWD=qazwsx123!;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

@app.route("/")
def show_orders():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        query = """
            SELECT TOP 10
                project_kablan_tb.projectname,
                project_dayarim_tb.familyname,
                project_dayarim_tb.orderno,
                sell_order_tb.tipul,
                sell_order_tb.totalpaid,
                sell_order_tb.orderdate
            FROM
                project_kablan_tb
                INNER JOIN project_detail_tb ON project_kablan_tb.kodkablan = project_detail_tb.kablantb
                INNER JOIN project_dayarim_tb ON project_detail_tb.kodproject = project_dayarim_tb.projecttb
                INNER JOIN sell_order_tb ON project_dayarim_tb.dayarim = sell_order_tb.dayarimtb
            WHERE
                project_dayarim_tb.orderno IS NOT NULL AND
                sell_order_tb.orderdate >= ?
            ORDER BY
                sell_order_tb.orderdate DESC;
        """

        cursor.execute(query, week_ago)
        rows = cursor.fetchall()

        html = """
        <h2 style="direction: rtl; font-family: Arial;">הזמנות מהשבוע האחרון</h2>
        <table border="1" dir="rtl" style="font-family: Arial; border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <th>שם פרויקט</th>
                <th>שם משפחה</th>
                <th>מס׳ הזמנה</th>
                <th>טיפול</th>
                <th>סכום</th>
                <th>תאריך</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row.projectname }}</td>
                <td>{{ row.familyname }}</td>
                <td>{{ row.orderno }}</td>
                <td>{{ row.tipul }}</td>
                <td>{{ row.totalpaid }}</td>
                <td>{{ row.orderdate.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </table>
        """
        return render_template_string(html, rows=rows)

    except Exception as e:
        return f"<h2>שגיאה:</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
