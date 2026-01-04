import random
import copy
import time


# ==========================================
# ESTRUCTURA DE DATOS
# ==========================================


class Equipo:
    def __init__(self, nombre, confederacion, bombo, grupo_fijo=None, ranking_top=None):
        self.nombre = nombre
        self.confederacion = confederacion  # String simple
        self.bombo = bombo
        self.grupo_fijo = grupo_fijo
        self.ranking_top = ranking_top  # 1, 2, 3, 4 o None

    def __repr__(self):
        # Muestra info útil al imprimir
        r = f" [R#{self.ranking_top}]" if self.ranking_top else ""
        f = f" (Fijo:{self.grupo_fijo})" if self.grupo_fijo else ""
        return f"{self.nombre}{r}{f}"


def generar_datos_usuario():
    equipos = []

    # --- BOMBO 1: Cabezas de Serie ---
    # Anfitriones (Fijos en A, B, D según realidad, o ajustamos si prefieres)
    # Asumimos que siguen fijos para mantener realismo estructural
    equipos.append(Equipo("México", ["CONCACAF"], 1, grupo_fijo="A"))
    equipos.append(Equipo("Canadá", ["CONCACAF"], 1, grupo_fijo="B"))
    equipos.append(Equipo("USA", ["CONCACAF"], 1, grupo_fijo="D"))

    # El TOP 4
    equipos.append(Equipo("España", ["UEFA"], 1, ranking_top=1))
    equipos.append(Equipo("Argentina", ["CONMEBOL"], 1, ranking_top=2))
    equipos.append(Equipo("Francia", ["UEFA"], 1, ranking_top=3))
    equipos.append(Equipo("Inglaterra", ["UEFA"], 1, ranking_top=4))

    # Rellenar el resto del Bombo 1 (5 equipos más para llegar a 12)
    extras_b1 = [
        ("Brasil", ["CONMEBOL"]),
        ("Bélgica", ["UEFA"]),
        ("Portugal", ["UEFA"]),
        ("Países Bajos", ["UEFA"]),
        ("Alemania", ["UEFA"]),
    ]
    for nom, conf in extras_b1:
        equipos.append(Equipo(nom, conf, 1))

    # --- BOMBOS 2, 3, 4 (Relleno Genérico) ---

    config_restante = [
        # (Nombre, Conf, Bombo) - Bloques simulados
        ("Uruguay", ["CONMEBOL"], 2),
        ("Colombia", ["CONMEBOL"], 2),
        ("Croacia", ["UEFA"], 2),
        ("Marruecos", ["CAF"], 2),
        ("Japón", ["AFC"], 2),
        ("Suiza", ["UEFA"], 2),
        ("Senegal", ["CAF"], 2),
        ("Irán", ["AFC"], 2),
        ("Corea del Sur", ["AFC"], 2),
        ("Ecuador", ["CONMEBOL"], 2),
        ("Austria", ["UEFA"], 2),
        ("Australia", ["AFC"], 2),
        ("Noruega", ["UEFA"], 3),
        ("Panamá ", ["CONCACAF"], 3),
        ("Egipto", ["CAF"], 3),
        ("Argelia", ["CAF"], 3),
        ("Escocia", ["UEFA"], 3),
        ("Paraguay", ["CONMEBOL"], 3),
        ("Túnez", ["CAF"], 3),
        ("Costa de Marfil ", ["CAF"], 3),
        ("Uzbekistán", ["AFC"], 3),
        ("Catar", ["AFC"], 3),
        ("Arabia Saudita", ["AFC"], 3),
        ("Sudáfrica", ["CAF"], 3),
        ("Jordania", ["AFC"], 4),
        ("Cabo Verde", ["CAF"], 4),
        ("Ghana", ["CAF"], 4),
        ("Curazao", ["CONCACAF"], 4),
        ("Haití", ["CONCACAF"], 4),
        ("Nueva Zelanda", ["OFC"], 4),
        ("Repesca Intercontinetal llave A", ["CAF", "CONCACAF", "OFC"], 4),
        ("Repesca Intercontinetal llave B", ["CONCACAF", "CONMEBOL", "AFC"], 4),
        ("A de la Repesca UEFA", ["UEFA"], 4),
        ("B de la Repesca UEFA", ["UEFA"], 4),
        ("C de la Repesca UEFA", ["UEFA"], 4),
        ("D de la Repesca UEFA", ["UEFA"], 4),
    ]
    for nombre, conf, bombo in config_restante:
        equipos.append(Equipo(nombre, conf, bombo))
    return equipos


# ==========================================
# EL MOTOR (FITNESS Y VALIDACIÓN)
# ==========================================


def obtener_itinerario(indice_grupo):
    """
    Retorna 1 o 2 dependiendo del grupo.
    Itinerario 1: D(3), E(4), F(5), G(6), H(7), I(8)
    Itinerario 2: A(0), B(1), C(2), J(9), K(10), L(11)
    """
    itin_1_indices = {3, 4, 5, 6, 7, 8}
    if indice_grupo in itin_1_indices:
        return 1
    return 2


def calcular_fitness(sorteo):
    """
    Calcula la penalización total de un sorteo (cromosoma).
    0 = Sorteo válido.
    return: penalizacion
    """
    penalizacion = 0

    # Constantes de Penalización (Pesos)
    PENALTY_CONF_LIMIT = 1000  # Conflicto de confederación (Grave)
    PENALTY_UEFA_LIMIT = 500  # Más de 2 europeos
    PENALTY_ITINERARY = 500  # Top seeds chocando antes de la final

    # Rastrear dónde cayeron los Top seeds {ranking: indice_grupo}
    ubicacion_tops = {}

    # --- 1. Bucle por Grupos ---
    for i, grupo in enumerate(sorteo):

        # A. Revisar límite de UEFA (Máximo 2)
        # Contamos cuántos equipos tienen 'UEFA' en su lista de confederaciones
        uefa_count = sum(1 for equipo in grupo if ["UEFA"] in equipo.confederacion)

        if uefa_count > 2:
            # Penalizamos para corregirlo
            penalizacion += PENALTY_UEFA_LIMIT * (uefa_count - 2)

        # B. Revisar choques de Confederaciones (NO UEFA)
        # Usamos doble for para comparar todos contra todos en el grupo
        for j in range(len(grupo)):
            for k in range(j + 1, len(grupo)):
                equipo_a = grupo[j]
                equipo_b = grupo[k]

                # Intersección de conjuntos:
                # Si Equipo A es ['CONMEBOL'] y Equipo B (Repesca) es ['CONMEBOL', 'AFC']
                # La intersección es {'CONMEBOL'} -> ¡Conflicto!
                set_a = set(equipo_a.confederacion)
                set_b = set(equipo_b.confederacion)
                interseccion = set_a.intersection(set_b)

                # Si hay intersección y NO es UEFA (porque UEFA permite 2), penalizamos
                # Nota: Si ambos son UEFA, 'UEFA' estará en la intersección,
                # pero eso ya lo controlamos arriba con uefa_count.
                conflicto_real = [c for c in interseccion if c != "UEFA"]

                if conflicto_real:
                    penalizacion += PENALTY_CONF_LIMIT

        # C. Guardar ubicación de Tops para la fase 2
        for equipo in grupo:
            if equipo.ranking_top:
                ubicacion_tops[equipo.ranking_top] = i

    # --- 2. Penalizaciones de Itinerario (Bracket) ---

    # Regla: Top 1 y Top 2 deben ir por lados opuestos del itinerario
    if 1 in ubicacion_tops and 2 in ubicacion_tops:
        it_1 = obtener_itinerario(ubicacion_tops[1])
        it_2 = obtener_itinerario(ubicacion_tops[2])

        if it_1 == it_2:
            penalizacion += PENALTY_ITINERARY

    # Regla: Top 3 y Top 4 deben ir por lados opuestos del itinerario
    if 3 in ubicacion_tops and 4 in ubicacion_tops:
        it_3 = obtener_itinerario(ubicacion_tops[3])
        it_4 = obtener_itinerario(ubicacion_tops[4])

        if it_3 == it_4:
            penalizacion += PENALTY_ITINERARY

    return penalizacion


# ==========================================
# ALGORITMO GENÉTICO (CON CROSSOVER Y MUTACIÓN)
# ==========================================


def crear_individuo(lista_equipos):
    # Crear un individuo (sorteo) válido inicial
    bombos = {1: [], 2: [], 3: [], 4: []}
    # Distribuir equipos por bombo
    for eq in lista_equipos:
        bombos[eq.bombo].append(eq)
    # Asignar equipos a grupos
    grupos = [[] for _ in range(12)]
    for b in range(1, 5):
        equipos = bombos[b]
        # Mezclar para aleatoriedad
        random.shuffle(equipos)
        pendientes = []
        for eq in equipos:
            if eq.grupo_fijo:
                # Asignar al grupo fijo y saltar (convierte letra del grupo a índice)
                idx = ord(eq.grupo_fijo) - 65
                grupos[idx].append(eq)
            else:
                pendientes.append(eq)
        idx_p = 0
        # Asignar restantes de este bombo
        for g_idx in range(12):
            if len(grupos[g_idx]) < b:
                grupos[g_idx].append(pendientes[idx_p])
                idx_p += 1
    return grupos


def seleccion_torneo(evaluados, k=3):
    """
    Selecciona 'k' individuos al azar y devuelve el que tiene menor costo (fitness).
    """
    candidatos = random.sample(evaluados, k)
    # Retornamos el individuo (índice 1) del candidato con menor score (índice 0)
    ganador = min(candidatos, key=lambda x: x[0])
    return ganador[1]


def seleccion_ruleta(evaluados):
    """
    Input: Lista de tuplas (fitness, individuo)
    Selección proporcional al fitness (Ruleta).
    Como buscamos MINIMIZAR el costo, invertimos el valor.
    Score 0 -> Peso muy alto. Score 500 -> Peso bajo.
    """
    # Separamos los individuos de sus costos para pasarlos a la función
    individuos = [item[1] for item in evaluados]
    costos = [item[0] for item in evaluados]

    # Invertimos los costos para obtener pesos (Mayor peso = Mayor probabilidad)
    pesos = [1.0 / (1.0 + c) for c in costos]
    # Se suma uno para evitar división por cero

    # La función choices de 3 argumentos (población, pesos, cantidad)
    seleccionado = random.choices(population=individuos, weights=pesos, k=1)[0]

    return seleccionado


def cruzar(padre1, padre2):
    """
    Operador de Cruce Estratificado (Uniform Crossover por Bombos).
    El hijo hereda la configuración entera de un bombo de uno de los padres.
    """
    # Hijos vacíos
    hijo1 = [[] for _ in range(12)]
    hijo2 = [[] for _ in range(12)]
    # Recorremos cada nivel de Bombo (0 a 3)
    for bombo_idx in range(4):
        # Decisión aleatoria: ¿Quién dona este bombo?
        if random.random() < 0.5:
            # Caso A: Hijo 1 hereda de Padre 1, Hijo 2 hereda de Padre 2
            donante_1 = padre1
            donante_2 = padre2
        else:
            # Caso B: Cruzado
            donante_1 = padre2
            donante_2 = padre1

        # Copiamos la fila entera de ese bombo a los hijos
        for g_idx in range(12):
            equipo_p1 = donante_1[g_idx][bombo_idx]
            equipo_p2 = donante_2[g_idx][bombo_idx]

            hijo1[g_idx].append(equipo_p1)
            hijo2[g_idx].append(equipo_p2)
    return hijo1, hijo2


def mutar(individuo, prob_mutacion):
    """
    Intenta mutar con probabilidad 'prob_mutacion'.
    """
    if random.random() > prob_mutacion:
        return individuo  # No muta

    # Si muta, hacemos el intercambio
    nuevo = copy.deepcopy(individuo)
    idx_g1, idx_g2 = random.sample(range(12), 2)
    bombo_idx = random.randint(0, 3)

    e1 = nuevo[idx_g1][bombo_idx]
    e2 = nuevo[idx_g2][bombo_idx]

    if not e1.grupo_fijo and not e2.grupo_fijo:
        nuevo[idx_g1][bombo_idx], nuevo[idx_g2][bombo_idx] = (
            nuevo[idx_g2][bombo_idx],
            nuevo[idx_g1][bombo_idx],
        )

    return nuevo


def ejecutar_ga_completo():
    # --- CONFIGURACIÓN ---
    POBLACION_TAM = 10
    GENERACIONES = 1000
    PROB_CROSSOVER = 0.8  # 80% probabilidad de cruce
    PROB_MUTACION = 0.2  # 20% probabilidad de mutación
    K_TORNEO = 2  # Tamaño del torneo para selección

    datos = generar_datos_usuario()
    poblacion = [crear_individuo(datos) for _ in range(POBLACION_TAM)]

    print(f"🧬 Iniciando GA (Pc={PROB_CROSSOVER}, Pm={PROB_MUTACION})...")

    for gen in range(GENERACIONES):
        # Evaluar Fitness
        # Guardamos (score, individuo)
        evaluados = [(calcular_fitness(ind), ind) for ind in poblacion]
        evaluados.sort(key=lambda x: x[0])

        best_score = evaluados[0][0]
        # Monitorización
        if gen % 100 == 0 or best_score == 0:
            print("======" * 20)
            print(f"Gen {gen}: Mejor Coste = {best_score}")

        if best_score == 0:
            print(f"✅ ¡SOLUCIÓN PERFECTA ENCONTRADA EN GEN {gen}!")
            return gen, evaluados[0][1]

        # Selección (Torneo simple)
        nueva_poblacion = []

        while len(nueva_poblacion) < POBLACION_TAM:
            # Seleccionar 2 padres al azar (Torneo)
            # padre1 = seleccion_torneo(evaluados, k=K_TORNEO)
            # padre2 = seleccion_torneo(evaluados, k=K_TORNEO)

            # OPCIÓN B: RULETA
            padre1 = seleccion_ruleta(evaluados)
            padre2 = seleccion_ruleta(evaluados)

            # Crossover
            if random.random() < PROB_CROSSOVER:
                hijo1, hijo2 = cruzar(padre1, padre2)
            else:
                hijo1, hijo2 = copy.deepcopy(padre1), copy.deepcopy(padre2)
            # Mutación
            hijo1 = mutar(hijo1, PROB_MUTACION)
            hijo2 = mutar(hijo2, PROB_MUTACION)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < POBLACION_TAM:
                nueva_poblacion.append(hijo2)
        poblacion = nueva_poblacion

    print("⚠️ Límite alcanzado. Devolviendo mejor aproximación.")
    return gen, evaluados[0][1]


# ==========================================
# EJECUCIÓN
# ==========================================
inicio = time.time()
gen, sorteo_final = ejecutar_ga_completo()
fin = time.time()

print("\n--- RESULTADO FINAL (Top 4 Separados) ---")
letras = "ABCDEFGHIJKL"
for i, grupo in enumerate(sorteo_final):
    b1 = grupo[0]
    itin = obtener_itinerario(i)
    tag = "ITIN_1" if itin == 1 else "ITIN_2"

    extra = ""
    if b1.ranking_top:
        extra = f" ⭐ RANK #{b1.ranking_top}"

    print(f"Grupo {letras[i]} [{tag}]: {b1.nombre}{extra}")
# ==========================================
# VISUALIZACIÓN FINAL COMPLETA
# ==========================================

print("\n" + "=" * 50)
print("       🏆 SORTEO MUNDIAL 2026 - RESULTADO 🏆")
print("=" * 50)

letras = "ABCDEFGHIJKL"

# Separamos visualmente los itinerarios
grupos_itin_1 = []
grupos_itin_2 = []

for i, grupo in enumerate(sorteo_final):
    itin = obtener_itinerario(i)
    data = (i, grupo)
    if itin == 1:
        grupos_itin_1.append(data)
    else:
        grupos_itin_2.append(data)


# Función auxiliar para imprimir un bloque de grupos
def imprimir_bloque(lista_grupos, nombre_itinerario):
    print(f"\n >>> {nombre_itinerario} <<<")
    print("-" * 40)
    for i, grupo in lista_grupos:
        letra = letras[i]

        # Cabecera del Grupo
        print(f"📁 GRUPO {letra}:")

        # Listar los 4 equipos
        for equipo in grupo:
            # Decoración
            icono = "⚽"
            if equipo.bombo == 1:
                icono = "🔴"  # Cabeza de serie

            extra = ""
            if equipo.ranking_top:
                extra = f" [Rank #{equipo.ranking_top}]"
            if equipo.grupo_fijo:
                extra = f" [Anfitrión]"

            # Formato: 🔴 Bombo 1: México (CONCACAF) [Anfitrión]
            print(
                f"   {icono} B{equipo.bombo}: {equipo.nombre:<15} ({equipo.confederacion}){extra}"
            )
        print("")  # Espacio entre grupos


# Imprimimos
imprimir_bloque(grupos_itin_1, "ITINERARIO 1 (Lado Izquierdo)")
imprimir_bloque(grupos_itin_2, "ITINERARIO 2 (Lado Derecho)")

# Verificación rápida de errores visual
print("=" * 50)
errores = calcular_fitness(sorteo_final)
if errores == 0:
    print("✅ SORTEO VÁLIDO: Se cumplen reglas de confederaciones y de itinerarios.")
else:
    print(f"⚠️ SORTEO INVÁLIDO: Penalización de {errores} puntos.")
# ==========================================
# TIEMPO DE EJECUCIÓN
# ==========================================
tiempo_total = fin - inicio
print(f"\n⏱️ Tiempo de Ejecución: {tiempo_total:.4f} segundos")
print(f"Generaciones: {gen}")
