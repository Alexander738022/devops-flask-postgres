from flask import Flask
import psycopg2

app = Flask(__name__)

VERSION = "3.0.0"

@app.route("/")
def inicio():

    try:
        conexion = psycopg2.connect(
            host="db",
            database="empresa",
            user="admin",
            password="admin123"
        )

        cursor = conexion.cursor()

        # Obtener versión de PostgreSQL
        cursor.execute("SELECT version();")
        version_postgres = cursor.fetchone()[0]

        # Obtener clientes
        cursor.execute("SELECT id, nombre FROM clientes ORDER BY id;")
        clientes = cursor.fetchall()

        filas = ""

        for cliente in clientes:
            filas += f"""
            <tr>
                <td>{cliente[0]}</td>
                <td>{cliente[1]}</td>
            </tr>
            """

        total_clientes = len(clientes)

        cursor.close()
        conexion.close()

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DevOps Flask PostgreSQL</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f9;
                    margin: 40px;
                }}

                .container {{
                    max-width: 900px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
                }}

                h1 {{
                    color: #0d6efd;
                }}

                h2 {{
                    color: #198754;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}

                th {{
                    background-color: #0d6efd;
                    color: white;
                }}

                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}

                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}

                .info {{
                    background-color: #e9f7ef;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}

            </style>
        </head>

        <body>

            <div class="container">

                <h1>🚀 Aplicación Flask + PostgreSQL</h1>

                <h2>Versión {VERSION}</h2>

                <div class="info">
                    <p><strong>Estado:</strong> Conexión exitosa a PostgreSQL ✅</p>
                    <p><strong>Total de clientes:</strong> {total_clientes}</p>
                </div>

                <h3>Clientes registrados</h3>

                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                        </tr>
                    </thead>

                    <tbody>
                        {filas}
                    </tbody>
                </table>

                <br>

                <h3>Información del servidor PostgreSQL</h3>

                <p>{version_postgres}</p>

            </div>

        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h1>Error de conexión ❌</h1>
        <p>{str(e)}</p>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)