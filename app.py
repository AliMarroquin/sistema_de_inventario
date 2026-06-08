from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# CONEXION A POSTGRESQL
conexion = psycopg2.connect(
    host="localhost",
    database="inventario",
    user="postgres",
    password="kln*00hb.",
    port="5432"
)

cursor = conexion.cursor()

#====================#
#  DASHBOARD #
#====================#

@app.route('/')
def dashboard():

    # Total equipos
    cursor.execute("SELECT COUNT(*) FROM equipos")
    total_equipos = cursor.fetchone()[0]

    # Equipos activos
    cursor.execute("""
        SELECT COUNT(*)
        FROM equipos
        WHERE estado = 'Activo'
    """)
    equipos_activos = cursor.fetchone()[0]

    # Usuarios asignados
    cursor.execute("""
        SELECT COUNT(DISTINCT usuario_asignado)
        FROM equipos
        WHERE usuario_asignado IS NOT NULL
        AND usuario_asignado <> ''
    """)
    usuarios_asignados = cursor.fetchone()[0]

    # Ubicaciones
    cursor.execute("""
        SELECT COUNT(DISTINCT ubicacion)
        FROM equipos
        WHERE ubicacion IS NOT NULL
        AND ubicacion <> ''
    """)
    ubicaciones = cursor.fetchone()[0]

    return render_template(
        'dashboard.html',
        total_equipos=total_equipos,
        equipos_activos=equipos_activos,
        usuarios_asignados=usuarios_asignados,
        ubicaciones=ubicaciones
    )

# INVENTARIO
@app.route('/inventario')
def inventario():
    
    estado = request.args.get('estado')

    if estado:
        cursor.execute("SELECT * FROM equipos WHERE estado = %s", (estado,))

    else:
        cursor.execute("SELECT * FROM equipos")


    equipos = cursor.fetchall()

    return render_template(
        'inventario.html',
        equipos=equipos)


# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        tipo_equipo = request.form['tipo_equipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        procesador = request.form['procesador']
        ram = request.form['ram']
        disco_duro = request.form['disco_duro']
        sistema_operativo = request.form['sistema_operativo']
        software_instalado = request.form['software_instalado']
        usuario_asignado = request.form['usuario_asignado']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        observaciones = request.form['onservaciones']

        cursor.execute("""
            INSERT INTO equipos (
                tipo_equipo,
                marca,
                modelo,
                numero_serie,
                procesador,
                ram,
                disco_duro,
                sistema_operativo,
                software_instalado,
                usuario_asignado,
                ubicacion,
                estado
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            tipo_equipo,
            marca,
            modelo,
            numero_serie,
            procesador,
            ram,
            disco_duro,
            sistema_operativo,
            software_instalado,
            usuario_asignado,
            ubicacion,
            estado
        ))

        conexion.commit()

        return redirect('/inventario')

    return render_template('registro.html')

###CONEXION A VER_EQUIPO###
@app.route('/ver/<int:id>')
def ver_equipo(id):

    cursor.execute(
        "SELECT * FROM equipos WHERE id = %s",
        (id,)
    )
    equipo = cursor.fetchone()

    cursor.execute(
        """
        SELECT descripcion, fecha
        FROM historial
        WHERE equipo_id = %s
        ORDER BY fecha DESC
        """,
        (id,)
    )
    historial = cursor.fetchall()

    return render_template(
        'ver_equipo.html',
        equipo=equipo,
        historial=historial
    )

#------------------#
#------------------#
#-Editar_registro-#
#------------------#

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    if request.method == 'POST':

        tipo_equipo = request.form['tipo_equipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        procesador = request.form['procesador']
        ram = request.form['ram']
        disco_duro = request.form['disco_duro']
        sistema_operativo = request.form['sistema_operativo']
        software_instalado = request.form['software_instalado']
        usuario_asignado = request.form['usuario_asignado']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']

        cursor.execute("""
            UPDATE equipos
            SET
                tipo_equipo = %s,
                marca = %s,
                modelo = %s,
                numero_serie = %s,
                procesador = %s,
                ram = %s,
                disco_duro = %s,
                sistema_operativo = %s,
                software_instalado = %s,
                usuario_asignado = %s,
                ubicacion = %s,
                estado = %s
            WHERE id = %s
        """, (
            tipo_equipo,
            marca,
            modelo,
            numero_serie,
            procesador,
            ram,
            disco_duro,
            sistema_operativo,
            software_instalado,
            usuario_asignado,
            ubicacion,
            estado,
            id
        ))

        cursor.execute("""
            INSERT INTO historial
            (equipo_id, descripcion)
            VALUES (%s, %s)
        """, (
            id,
            'Se modificó la información del equipo'
        ))

        conexion.commit()

        return redirect('/inventario')

    cursor.execute(
        "SELECT * FROM equipos WHERE id = %s",
        (id,)
    )

    equipo = cursor.fetchone()

    return render_template(
        'editar_equipo.html',
        equipo=equipo
    )


if __name__ == '__main__':
    app.run(debug=True)