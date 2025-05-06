from flask import Flask, render_template_string
import psycopg2

app = Flask(__name__)

# פרטי התחברות למסד PostgreSQL בענן
pg_conn_str = "host=dpg-d0blet2dbo4c73cs5nfg-a.frankfurt-postgres.render.com dbname=orders_2ia3 user=orders_user password=iyuviUrVororwVqpoKqR2lyVBM3UlWSq"

@app.route("/")
def show_orders():
    try:
        conn = psycopg2.connect(pg_conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT projectname, familyname, orderno, tipul, totalpaid, orderdate
            FROM week_order
            ORDER BY orderdate DESC
            LIMIT 50;
        """)
        rows = cursor.fetchall()
        conn.close()

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
        return f"<h2>❌ שגיאה:</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
