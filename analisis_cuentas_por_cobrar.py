# Importamos Pandas para analizar los datos.
import pandas as pd

# Importamos Matplotlib para crear graficos.
import matplotlib.pyplot as plt

# Importamos Path para trabajar con carpetas
# y rutas de archivos.
from pathlib import Path

# -----------------------------------------------------
# CONFIGURACION DE LA CARPETA DE GRAFICOS
# -----------------------------------------------------

# Identificamos la carpeta donde se encuentra
# nuestro archivo Python del proyecto.
carpeta_proyecto = Path(__file__).resolve().parent

# Indicamos que los graficos se guardaran
# en la subcarpeta llamada "Gráficos".
carpeta_graficos = carpeta_proyecto / "Gráficos"

# Creamos la carpeta si todavia no existe.
# Si ya existe, Python no mostrara un error.
carpeta_graficos.mkdir(parents=True, exist_ok=True)

# =====================================================
# CLASE 16: PROYECTO FINAL DE PYTHON PARA DATA ANALYTICS
# PROYECTO: ANALISIS DE CUENTAS POR COBRAR
# =====================================================

# OBJETIVO:
# Analizar la cartera de clientes utilizando
# Python, Pandas y Matplotlib.

# -----------------------------------------------------
# PASO 1: IMPORTAR LAS BIBLIOTECAS
# -----------------------------------------------------

# Pandas permite crear, limpiar y analizar tablas.
import pandas as pd

# Matplotlib permite crear graficos financieros.
import matplotlib.pyplot as plt


# -----------------------------------------------------
# PASO 2: CREAR NUESTRA BASE DE DATOS
# -----------------------------------------------------

# Creamos un diccionario con los datos de
# ocho facturas pendientes de cobro.

datos = {
    "Factura": [
        "F001", "F002", "F003", "F004",
        "F005", "F006", "F007", "F008"
    ],

    "Cliente": [
        "Ana", "Luis", "Carlos", "María",
        "Pedro", "Sofía", "Ana", "Luis"
    ],

    "Valor USD": [
        1200, 2500, 800, 1800,
        950, 3200, 600, 1500
    ],

    "Fecha Vencimiento": [
        "2026-10-25",
        "2026-11-20",
        "2026-09-15",
        "2026-11-13",
        "2026-08-01",
        "2026-10-05",
        "2026-12-01",
        "2026-07-15"
    ]
}

# Convertimos el diccionario en un DataFrame.
df = pd.DataFrame(datos)


# -----------------------------------------------------
# PASO 3: VISUALIZAR LA INFORMACION
# -----------------------------------------------------

# Mostramos todas las facturas en la terminal.
print("\nBASE DE DATOS DE CUENTAS POR COBRAR:")
print(df.to_string(index=False))

# Mostramos las primeras cinco filas para
# comprobar que los datos se cargaron correctamente.
print("\nPRIMERAS CINCO FACTURAS:")
print(df.head())

# Mostramos el numero de filas y columnas.
print("\nDIMENSIONES DE LA BASE DE DATOS:")
print(df.shape)

# -----------------------------------------------------
# PASO 4: LIMPIEZA Y VALIDACION DE DATOS
# -----------------------------------------------------

# 1. Identificamos los valores faltantes.
# isnull() detecta las celdas vacias.
# sum() cuenta cuantos valores faltan por columna.

print("\nVALORES FALTANTES:")
print(df.isnull().sum())


# 2. Comprobamos si existen facturas duplicadas.
# duplicated() identifica codigos de factura
# que aparecen mas de una vez.
# keep=False permite mostrar todas las repeticiones.

# -----------------------------------------------------
# IDENTIFICAR FACTURAS DUPLICADAS
# -----------------------------------------------------

# duplicated() busca números de factura repetidos.
# subset=["Factura"] indica la columna que revisamos.
# keep=False permite identificar todas las
# apariciones de las facturas duplicadas.

facturas_duplicadas = df[
    df.duplicated(subset=["Factura"], keep=False)
]

# Mostramos las facturas duplicadas en la terminal.
print("\nFACTURAS DUPLICADAS:")
print(facturas_duplicadas)

# -----------------------------------------------------
# PASO 5: CALCULAR LOS DIAS DE ATRASO
# -----------------------------------------------------

# 1. Convertimos la columna de vencimiento a fechas.
# Esto permite realizar operaciones entre fechas.

df["Fecha Vencimiento"] = pd.to_datetime(
    df["Fecha Vencimiento"]
)

# 2. Establecemos la fecha de corte del reporte.
# Usamos una fecha fija para que los resultados
# del ejercicio sean siempre los mismos.

fecha_corte = pd.to_datetime("2026-11-13")

# 3. Calculamos la diferencia de dias.
# Restamos la fecha de vencimiento a la fecha
# de corte y extraemos el numero de dias.
#
# Positivo: factura vencida.
# Cero: vence hoy.
# Negativo: factura vigente.

df["Dias Diferencia"] = (
    fecha_corte - df["Fecha Vencimiento"]
).dt.days

# 4. Calculamos los dias de atraso.
# clip(lower=0) convierte los valores negativos
# en cero y conserva los positivos.

df["Dias Atraso"] = df["Dias Diferencia"].clip(
    lower=0
)

# 5. Mostramos los resultados en la terminal.

print("\nREPORTE DE DIAS DE ATRASO:")
print(
    df[
        ["Factura", "Cliente", "Dias Diferencia", "Dias Atraso"]
    ].to_string(index=False)
)

# -----------------------------------------------------
# PASO 6: CLASIFICAR LA ANTIGUEDAD DE CARTERA
# -----------------------------------------------------

# 1. Creamos una funcion para clasificar las facturas.
# Recibimos la diferencia de dias de cada factura.
#
# Negativo: factura vigente.
# Cero: vence hoy.
# Entre 1 y 30: vencida 1-30 dias.
# Entre 31 y 60: vencida 31-60 dias.
# Mayor a 60: vencida +60 dias.

def clasificar_antiguedad(dias):
    if dias < 0:
        return "Vigente"
    elif dias == 0:
        return "Vence hoy"
    elif dias <= 30:
        return "Vencida 1-30 dias"
    elif dias <= 60:
        return "Vencida 31-60 dias"
    else:
        return "Vencida +60 dias"


# 2. Aplicamos la funcion a cada factura.
# apply() ejecuta nuestra funcion para cada
# valor de la columna "Dias Diferencia".

df["Antiguedad"] = df["Dias Diferencia"].apply(
    clasificar_antiguedad
)


# 3. Mostramos el reporte de antiguedad.
# Seleccionamos las columnas mas importantes
# para revisar los resultados.

print("\nREPORTE DE ANTIGUEDAD DE CARTERA:")
print(
    df[
        ["Factura", "Cliente", "Dias Atraso", "Antiguedad"]
    ].to_string(index=False)
)

# PASO 7: CALCULAR INDICADORES FINANCIEROS (KPIs)
# -----------------------------------------------------

# 1. Calculamos la cartera total.
# sum() suma los importes de todas las facturas,
# tanto vigentes como vencidas.

cartera_total = df["Valor USD"].sum()


# 2. Filtramos las facturas vencidas.
# Seleccionamos solamente aquellas con
# mas de cero dias de atraso.

facturas_vencidas = df[df["Dias Atraso"] > 0]


# 3. Calculamos la cartera vencida.
# Sumamos los importes de las facturas
# que ya superaron su fecha de vencimiento.

cartera_vencida = facturas_vencidas["Valor USD"].sum()


# 4. Calculamos la cartera no vencida.
# Restamos la cartera vencida a la cartera total.
# Incluye las facturas vigentes y las que vencen hoy.

cartera_no_vencida = cartera_total - cartera_vencida


# 5. Calculamos el porcentaje de cartera vencida.
# Dividimos la cartera vencida entre la cartera total
# y multiplicamos por 100.
# Verificamos que el total sea mayor que cero
# para evitar una division entre cero.

if cartera_total > 0:
    porcentaje_vencido = (
        cartera_vencida / cartera_total
    ) * 100
else:
    porcentaje_vencido = 0


# 6. Contamos las facturas vencidas.
# len() devuelve el numero de filas
# del DataFrame filtrado.

cantidad_vencidas = len(facturas_vencidas)


# 7. Mostramos los indicadores financieros.
# :.2f presenta los valores con dos decimales.

print("\nINDICADORES FINANCIEROS - PROYECTO FINAL")
print("------------------------------------------")
print(f"Cartera total: ${cartera_total:.2f}")
print(f"Cartera vencida: ${cartera_vencida:.2f}")
print(f"Cartera no vencida: ${cartera_no_vencida:.2f}")
print(f"Porcentaje vencido: {porcentaje_vencido:.2f}%")
print(f"Cantidad de facturas vencidas: {cantidad_vencidas}")

# -----------------------------------------------------
# PASO 8: AGRUPAR LA CARTERA POR ANTIGUEDAD
# -----------------------------------------------------

# 1. Agrupamos las facturas por su clasificacion
# de antiguedad utilizando groupby().
#
# sum() calcula el importe total pendiente
# correspondiente a cada categoria.

cartera_por_antiguedad = df.groupby(
    "Antiguedad"
)["Valor USD"].sum()


# 2. Mostramos el resumen financiero.
# Cada fila representa un rango de antiguedad
# con su respectivo importe pendiente.

print("\nCARTERA POR ANTIGUEDAD:")
print(cartera_por_antiguedad)


# 3. Seleccionamos solamente las facturas vencidas.
# Estas fueron identificadas en el Paso 7.

# Agrupamos las facturas vencidas por antiguedad
# para analizar donde se concentra el saldo.

resumen_vencido = facturas_vencidas.groupby(
    "Antiguedad"
)["Valor USD"].sum()


# 4. Identificamos el rango con mayor saldo vencido.
# idxmax() devuelve el nombre del rango
# que tiene el importe mas alto.
#
# max() devuelve el valor de ese importe.

if not resumen_vencido.empty:
    rango_mayor_saldo = resumen_vencido.idxmax()
    importe_mayor_saldo = resumen_vencido.max()

    # Mostramos los resultados en la terminal.
    print("\nRANGO CON MAYOR SALDO VENCIDO:")
    print(f"Rango: {rango_mayor_saldo}")
    print(f"Importe: ${importe_mayor_saldo:.2f}")
else:
    print("\nNo existen facturas vencidas.")

# -----------------------------------------------------
# PASO 9: CREAR GRAFICOS FINANCIEROS
# -----------------------------------------------------

# GRAFICO 1: CARTERA POR ANTIGUEDAD

# 1. Definimos el orden de las categorias.
# Esto permite mostrar los rangos en orden
# financiero y no alfabetico.

orden_antiguedad = [
    "Vigente",
    "Vence hoy",
    "Vencida 1-30 dias",
    "Vencida 31-60 dias",
    "Vencida +60 dias"
]

# 2. Organizamos los importes segun ese orden.
# reindex() coloca las categorias en el orden
# indicado y fill_value=0 completa grupos ausentes.

datos_grafico = cartera_por_antiguedad.reindex(
    orden_antiguedad,
    fill_value=0
)

# 3. Creamos una nueva figura.
# figsize establece el tamaño del grafico.

plt.figure(figsize=(11, 6))

# 4. Creamos el grafico de barras.
# Los nombres de los grupos aparecen en el eje X
# y los importes pendientes en el eje Y.

barras = plt.bar(
    datos_grafico.index,
    datos_grafico.values,
    color="steelblue"
)

# 5. Mostramos el importe encima de cada barra.

plt.bar_label(barras, fmt="$%.0f", padding=3)

# 6. Agregamos titulo y etiquetas.

plt.title("Proyecto final: Cartera por antiguedad")
plt.xlabel("Antiguedad de cartera")
plt.ylabel("Saldo pendiente USD")

# 7. Giramos las etiquetas del eje X para
# evitar que los nombres se superpongan.

plt.xticks(rotation=20, ha="right")

# 8. Ajustamos los espacios del grafico.

plt.tight_layout()

# 9. Guardamos el grafico en formato PNG
# antes de mostrarlo en pantalla.

# Guardamos el grafico de antiguedad
# dentro de la carpeta "Gráficos" del proyecto.

plt.savefig(
    carpeta_graficos / "Proyecto_Final_Cartera_Antiguedad.png",
    dpi=300,
    bbox_inches="tight"
)


# 10. Mostramos y cerramos la figura.
# Cierra la ventana para continuar.

plt.show()
plt.close()


# -----------------------------------------------------
# GRAFICO 2: CARTERA VENCIDA VS. NO VENCIDA
# -----------------------------------------------------

# 1. Creamos las etiquetas del grafico circular.

estados = [
    "Cartera vencida",
    "Cartera no vencida"
]

# 2. Utilizamos los indicadores financieros
# calculados anteriormente en el Paso 7.

importes = [
    cartera_vencida,
    cartera_no_vencida
]

# 3. Creamos una nueva figura.

plt.figure(figsize=(8, 6))

# 4. Creamos el grafico circular.
# autopct muestra el porcentaje de cada grupo
# con un decimal.

plt.pie(
    importes,
    labels=estados,
    autopct="%1.1f%%",
    startangle=90
)

# 5. Agregamos el titulo y mantenemos
# la figura con forma circular.

plt.title("Proyecto final: Distribucion de cartera")
plt.axis("equal")

# 6. Ajustamos los espacios.

plt.tight_layout()

# 7. Guardamos el segundo grafico en PNG.

# Guardamos el grafico circular de distribucion
# de cartera dentro de la carpeta "Gráficos".

plt.savefig(
    carpeta_graficos / "Proyecto_Final_Distribucion_Cartera.png",
    dpi=300,
    bbox_inches="tight"
)

# 8. Mostramos y cerramos la figura.

plt.show()
plt.close()


datos_grafico = cartera_por_antiguedad.reindex(
    orden_antiguedad,
    fill_value=0
)

# -----------------------------------------------------
# PASO 10: CONCLUSIONES Y RECOMENDACIONES FINANCIERAS
# -----------------------------------------------------

# 1. Calculamos el saldo vencido por mas de 60 dias.
# Este grupo merece especial atencion debido
# a su mayor antiguedad.

cartera_mayor_60 = df.loc[
    df["Dias Diferencia"] > 60,
    "Valor USD"
].sum()


# 2. Calculamos que porcentaje representa
# la cartera mayor a 60 dias sobre el total.

if cartera_total > 0:
    porcentaje_mayor_60 = (
        cartera_mayor_60 / cartera_total
    ) * 100
else:
    porcentaje_mayor_60 = 0


# 3. Mostramos las conclusiones del proyecto.
# Utilizamos los indicadores calculados
# en los pasos anteriores.

print("\n==========================================")
print("INFORME EJECUTIVO - CUENTAS POR COBRAR")
print("==========================================")

print(f"Fecha de corte: {fecha_corte.date()}")
print(f"Cartera total: ${cartera_total:.2f}")
print(f"Cartera vencida: ${cartera_vencida:.2f}")
print(f"Porcentaje vencido: {porcentaje_vencido:.2f}%")
print(f"Cartera mayor a 60 dias: ${cartera_mayor_60:.2f}")
print(f"Porcentaje mayor a 60 dias: {porcentaje_mayor_60:.2f}%")


# 4. Generamos recomendaciones financieras.
# Si la cartera vencida supera el 50%,
# recomendamos reforzar las gestiones de cobro.

print("\nRECOMENDACIONES:")

if porcentaje_vencido > 50:
    print(
        "- Priorizar la recuperacion de cartera "
        "debido al alto porcentaje vencido."
    )
else:
    print(
        "- Mantener el seguimiento preventivo "
        "de las cuentas por cobrar."
    )

# 5. Evaluamos las facturas con mayor antiguedad.
# Su recuperacion requiere seguimiento prioritario.

if cartera_mayor_60 > 0:
    print(
        "- Revisar las facturas vencidas por "
        "mas de 60 dias y contactar a los clientes."
    )

# 6. Recomendamos seguimiento a los vencimientos
# para reducir el riesgo de nuevos atrasos.

print(
    "- Establecer recordatorios de pago "
    "antes de cada fecha de vencimiento."
)

print(
    "- Revisar semanalmente los indicadores "
    "de cartera y los compromisos de pago."
)
