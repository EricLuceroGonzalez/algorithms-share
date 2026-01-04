// ==========================================
// CLASES Y DATOS
// ==========================================

class Equipo {
  constructor(
    nombre,
    confederacion,
    bombo,
    grupoFijo = null,
    rankingTop = null
  ) {
    this.nombre = nombre;
    this.confederacion = confederacion;
    this.bombo = bombo;
    this.grupoFijo = grupoFijo;
    this.rankingTop = rankingTop;
  }
}

function generarDatosEquipos() {
  const equipos = [];

  equipos.push(new Equipo("México", ["CONCACAF"], 1, "A"));
  equipos.push(new Equipo("Canadá", ["CONCACAF"], 1, "B"));
  equipos.push(new Equipo("USA", ["CONCACAF"], 1, "D"));

  equipos.push(new Equipo("España", ["UEFA"], 1, null, 1));
  equipos.push(new Equipo("Argentina", ["CONMEBOL"], 1, null, 2));
  equipos.push(new Equipo("Francia", ["UEFA"], 1, null, 3));
  equipos.push(new Equipo("Inglaterra", ["UEFA"], 1, null, 4));

  const extrasB1 = [
    ["Brasil", ["CONMEBOL"]],
    ["Bélgica", ["UEFA"]],
    ["Portugal", ["UEFA"]],
    ["Países Bajos", ["UEFA"]],
    ["Alemania", ["UEFA"]],
  ];
  extrasB1.forEach(([nom, conf]) => equipos.push(new Equipo(nom, conf, 1)));

  const configRestante = [
    ["Uruguay", ["CONMEBOL"], 2],
    ["Colombia", ["CONMEBOL"], 2],
    ["Croacia", ["UEFA"], 2],
    ["Marruecos", ["CAF"], 2],
    ["Japón", ["AFC"], 2],
    ["Suiza", ["UEFA"], 2],
    ["Senegal", ["CAF"], 2],
    ["Irán", ["AFC"], 2],
    ["Corea del Sur", ["AFC"], 2],
    ["Ecuador", ["CONMEBOL"], 2],
    ["Austria", ["UEFA"], 2],
    ["Australia", ["AFC"], 2],
    ["Noruega", ["UEFA"], 3],
    ["Panamá", ["CONCACAF"], 3],
    ["Egipto", ["CAF"], 3],
    ["Argelia", ["CAF"], 3],
    ["Escocia", ["UEFA"], 3],
    ["Paraguay", ["CONMEBOL"], 3],
    ["Túnez", ["CAF"], 3],
    ["Costa de Marfil", ["CAF"], 3],
    ["Uzbekistán", ["AFC"], 3],
    ["Catar", ["AFC"], 3],
    ["Arabia Saudita", ["AFC"], 3],
    ["Sudáfrica", ["CAF"], 3],
    ["Jordania", ["AFC"], 4],
    ["Cabo Verde", ["CAF"], 4],
    ["Ghana", ["CAF"], 4],
    ["Curazao", ["CONCACAF"], 4],
    ["Haití", ["CONCACAF"], 4],
    ["Nueva Zelanda", ["OFC"], 4],
    ["Repesca IC-A", ["CAF", "CONCACAF", "OFC"], 4],
    ["Repesca IC-B", ["CONMEBOL", "CONCACAF", "AFC"], 4],
    ["Repesca UEFA-A", ["UEFA"], 4],
    ["Repesca UEFA-B", ["UEFA"], 4],
    ["Repesca UEFA-C", ["UEFA"], 4],
    ["Repesca UEFA-D", ["UEFA"], 4],
  ];

  configRestante.forEach(([nombre, conf, bombo]) =>
    equipos.push(new Equipo(nombre, conf, bombo))
  );

  return equipos;
}

// ==========================================
// ALGORITMO GENÉTICO
// ==========================================

export function obtenerItinerario(indiceGrupo) {
  const itin1Indices = new Set([3, 4, 5, 6, 7, 8]);
  return itin1Indices.has(indiceGrupo) ? 1 : 2;
}

function calcularFitness(sorteo) {
  let penalizacion = 0;
  const ubicacionTops = {};

  // Función auxiliar para determinar lado del cuadro (A-F vs G-L)
  const obtenerItinerario = (idx) => (idx < 6 ? 0 : 1);

  for (let i = 0; i < sorteo.length; i++) {
    const grupo = sorteo[i];
    const conteoConfs = {};

    for (const equipo of grupo) {
      // 1. Rastrear Tops (Igual que antes)
      if (equipo.rankingTop) ubicacionTops[equipo.rankingTop] = i;

      // 2. Contar Confederaciones (ADAPTADO)
      // Como 'equipo.confederacion' es un array, recorremos cada una.
      // Si es una Repesca con 3 opciones, sumará +1 a las 3 opciones.
      equipo.confederacion.forEach((conf) => {
        conteoConfs[conf] = (conteoConfs[conf] || 0) + 1;
      });
    }

    // 3. Evaluar Penalizaciones (Exactamente igual que tu código)
    for (const [conf, cant] of Object.entries(conteoConfs)) {
      if (conf === "UEFA") {
        if (cant > 2) penalizacion += 100;
      } else {
        // Aquí atrapamos el error:
        // Si hay un equipo de CONCACAF y entra una Repesca con opción CONCACAF,
        // el contador será 2 -> Penalización.
        if (cant > 1) penalizacion += 100;
      }
    }
  }

  // --- Lógica de Itinerario (Exactamente igual que tu código) ---

  if (ubicacionTops[1] !== undefined && ubicacionTops[2] !== undefined) {
    if (
      obtenerItinerario(ubicacionTops[1]) ===
      obtenerItinerario(ubicacionTops[2])
    ) {
      penalizacion += 500;
    }
  }

  if (ubicacionTops[3] !== undefined && ubicacionTops[4] !== undefined) {
    if (
      obtenerItinerario(ubicacionTops[3]) ===
      obtenerItinerario(ubicacionTops[4])
    ) {
      penalizacion += 500;
    }
  }

  return penalizacion;
}

function crearIndividuo(listaEquipos) {
  // Crear un individuo (sorteo) válido inicial recibiendo la lista de equipos
  // Creamos los bombos vacíos
  const bombos = { 1: [], 2: [], 3: [], 4: [] };
  // Distribuir equipos en cada bombo
  listaEquipos.forEach((eq) => bombos[eq.bombo].push(eq));
  // Creamos 12 grupos vacíos
  const grupos = Array.from({ length: 12 }, () => []);

  // Asignar equipos a grupos bombo por bombo
  for (let b = 1; b <= 4; b++) {
    const equipos = [...bombos[b]];
    equipos.sort(() => Math.random() - 0.5);

    // Array para los que no tienen grupo fijo
    const pendientes = [];
    for (const eq of equipos) {
      if (eq.grupoFijo) {
        // Convierte la letra del grupo a índice numérico
        const idx = eq.grupoFijo.charCodeAt(0) - 65;
        grupos[idx].push(eq);
      } else {
        pendientes.push(eq);
      }
    }
    // Asignar los equipos pendientes a los grupos que faltan de este bombo b
    let idxP = 0;
    for (let gIdx = 0; gIdx < 12; gIdx++) {
      if (grupos[gIdx].length < b) {
        grupos[gIdx].push(pendientes[idxP]);
        idxP++;
      }
    }
  }

  return grupos;
}

function seleccion_torneo(evaluados, k = 4) {
  const candidatos = [];
  for (let i = 0; i < k; i++) {
    candidatos.push(evaluados[Math.floor(Math.random() * evaluados.length)]);
  }
  candidatos.sort((a, b) => a[0] - b[0]);
  return candidatos[0][1];
}
function seleccionarPorRuleta(evaluados) {
  // 1. Calculamos la suma total de las "inversas" de los puntajes
  // Sumamos 1 al score para evitar división por cero si el score es 0 (perfecto)
  let totalWeight = 0;
  const weights = evaluados.map((item) => {
    const score = item[0];
    // Usamos 1/(score+1). Si score es 0, peso es 1. Si score es 1000, peso es 0.0009
    const weight = 1 / (score + 1);
    totalWeight += weight;
    return weight;
  });

  // 2. Tiramos la bolita en la ruleta
  let random = Math.random() * totalWeight;

  // 3. Buscamos dónde cayó
  for (let i = 0; i < evaluados.length; i++) {
    random -= weights[i];
    if (random <= 0) {
      return evaluados[i]; // Retornamos [score, individuo]
    }
  }

  // Fallback por errores de redondeo (retorna el último o el mejor)
  return evaluados[evaluados.length - 1];
}
function cruzar(padre1, padre2) {
  const hijo1 = Array.from({ length: 12 }, () => []);
  const hijo2 = Array.from({ length: 12 }, () => []);

  for (let bomboIdx = 0; bomboIdx < 4; bomboIdx++) {
    const [donante1, donante2] =
      Math.random() < 0.5 ? [padre1, padre2] : [padre2, padre1];
    for (let gIdx = 0; gIdx < 12; gIdx++) {
      hijo1[gIdx].push(donante1[gIdx][bomboIdx]);
      hijo2[gIdx].push(donante2[gIdx][bomboIdx]);
    }
  }

  return [hijo1, hijo2];
}

function mutar(individuo, probMutacion) {
  if (Math.random() > probMutacion) return individuo;

  const nuevo = individuo.map((g) => [...g]);
  const idxG1 = Math.floor(Math.random() * 12);
  const idxG2 = Math.floor(Math.random() * 12);
  const bomboIdx = Math.floor(Math.random() * 4);

  const e1 = nuevo[idxG1][bomboIdx];
  const e2 = nuevo[idxG2][bomboIdx];

  if (!e1.grupoFijo && !e2.grupoFijo) {
    [nuevo[idxG1][bomboIdx], nuevo[idxG2][bomboIdx]] = [
      nuevo[idxG2][bomboIdx],
      nuevo[idxG1][bomboIdx],
    ];
  }

  return nuevo;
}

export function ejecutarGA(onProgress) {
  const POBLACION_TAM = 100;
  const GENERACIONES = 1000;
  const PROB_CROSSOVER = 0.8;
  const PROB_MUTACION = 0.2;

  const datos = generarDatosEquipos();
  let poblacion = Array.from({ length: POBLACION_TAM }, () =>
    crearIndividuo(datos)
  );

  for (let gen = 0; gen < GENERACIONES; gen++) {
    let evaluados = poblacion.map((ind) => [calcularFitness(ind), ind]);
    evaluados.sort((a, b) => a[0] - b[0]);

    const bestScore = evaluados[0][0];

    if (gen % 100 === 0 || bestScore === 0) {
      onProgress(gen, bestScore);
    }

    if (bestScore === 0) {
      return { sorteo: evaluados[0][1], generacion: gen, costo: bestScore };
    }
    // Elitismo
    // const nuevaPoblacion = [evaluados[0][1]];
    const nuevaPoblacion = [];
    while (nuevaPoblacion.length < POBLACION_TAM) {
      // Seleccionamos dos padres independientemente
      const padreA = seleccionarPorRuleta(evaluados);
      const padreB = seleccionarPorRuleta(evaluados);

      let [hijo1, hijo2] =
        Math.random() < PROB_CROSSOVER
          ? cruzar(padreA[1], padreB[1])
          : [padreA[1].map((g) => [...g]), padreB[1].map((g) => [...g])];

      hijo1 = mutar(hijo1, PROB_MUTACION);
      hijo2 = mutar(hijo2, PROB_MUTACION);

      nuevaPoblacion.push(hijo1);
      if (nuevaPoblacion.length < POBLACION_TAM) nuevaPoblacion.push(hijo2);
    }

    poblacion = nuevaPoblacion;
  }

  const evaluadosFinal = poblacion.map((ind) => [calcularFitness(ind), ind]);
  evaluadosFinal.sort((a, b) => a[0] - b[0]);

  return {
    sorteo: evaluadosFinal[0][1],
    generacion: GENERACIONES,
    costo: evaluadosFinal[0][0],
  };
}
