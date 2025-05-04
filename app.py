from flask import Flask, render_template_string
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def show_orders():
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()

        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        query = """
            SELECT projectname, familyname, orderno, tipul, totalpaid, orderdate
            FROM orders
            WHERE orderdate >= ?
            ORDER BY orderdate DESC
            LIMIT 10
        """

        cursor.execute(query, (week_ago,))
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
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
            </tr>
            {% endfor %}
        </table>
        """
        return render_template_string(html, rows=rows)

    except Exception as e:
        return f"<h2>שגיאה:</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
