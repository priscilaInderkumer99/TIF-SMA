import json
import time
import random
from pyswip import Prolog

# ---------------------------
# Carga de reglas Prolog
# ---------------------------
prolog = Prolog()
prolog.consult("reglas_sptb.pl")

# ---------------------------
# Clase base
# ---------------------------
class Agente:
    def __init__(self, nombre):
        self.nombre = nombre
    def enviar(self, tipo, receptor, contenido):
        return {"performativa": tipo, "emisor": self.nombre,
                "receptor": receptor, "contenido": contenido}

# ---------------------------
# Agentes especialistas
# ---------------------------
class AgenteTranscriptomico(Agente):
    def analizar(self, paciente):
        print("Agente Transcriptómico analizando datos RNA-seq...")
        time.sleep(1)
        riesgo = random.uniform(0.7, 0.85)
        if paciente["fetal_sex"] == "male": riesgo *= 1.15
        else: riesgo *= 0.95
        riesgo = min(riesgo, 1.0)
        return self.enviar("INFORMAR", "Coordinador", {
            "riesgo": round(riesgo, 2),
            "confianza": round(random.uniform(0.85, 0.95), 2),
            "evidencia": "Activación de vías inflamatorias y estrés oxidativo"
        })

class AgenteMetabolomico(Agente):
    def analizar(self, paciente):
        print("Agente Metabolómico evaluando metabolitos placentarios...")
        time.sleep(1)
        riesgo = random.uniform(0.6, 0.8)
        if paciente["gestational_age"] < 32: riesgo += 0.05
        riesgo = min(riesgo, 1.0)
        return self.enviar("INFORMAR", "Coordinador", {
            "riesgo": round(riesgo, 2),
            "confianza": round(random.uniform(0.8, 0.9), 2),
            "evidencia": "Acilcarnitinas elevadas y disfunción mitocondrial"
        })

class AgenteClinico(Agente):
    def analizar(self, paciente):
        print("Agente Clínico integrando factores maternos y fetales...")
        time.sleep(1)
        riesgo = random.uniform(0.6, 0.7)
        if paciente["ethnicity"].lower() == "afroamericana": riesgo += 0.05
        if paciente["gestational_age"] < 32: riesgo += 0.05
        riesgo = min(riesgo, 1.0)
        return self.enviar("INFORMAR", "Coordinador", {
            "riesgo": round(riesgo, 2),
            "confianza": round(random.uniform(0.8, 0.9), 2),
            "evidencia": "Edad gestacional baja, feto masculino, etnia afroamericana"
        })

# ---------------------------
# Coordinador de decisiones
# ---------------------------
class Coordinador(Agente):
    def __init__(self, agentes):
        super().__init__("Coordinador")
        self.agentes = agentes

    def ejecutar(self, paciente):
        print("\nIniciando análisis distribuido...\n")
        resultados = []
        for a in self.agentes:
            r = a.analizar(paciente)
            resultados.append(r)
            print(f"{a.nombre}: riesgo={r['contenido']['riesgo']} "
                  f"| confianza={r['contenido']['confianza']}")
        return resultados

    def discrepancia(self, resultados, umbral=0.15):
        r = [x["contenido"]["riesgo"] for x in resultados]
        return (max(r) - min(r)) > umbral

    def negociar_zeuthen(self, resultados):
        print("\nNegociación Zeuthen iniciada...")
        r_t = resultados[0]["contenido"]["riesgo"]
        r_m = resultados[1]["contenido"]["riesgo"]
        for ronda in range(1, 4):
            print(f"Ronda {ronda}: rT={r_t:.2f}, rM={r_m:.2f}")
            f_t = (r_t - r_m) / (1.0 - r_t)
            f_m = (r_t - r_m) / (1.0 - r_m)
            if f_m < f_t:
                r_m += 0.04
                print("  ➜ Cede Agente Metabolómico")
            else:
                r_t -= 0.03
                print("  ➜ Cede Agente Transcriptómico")
            if abs(r_t - r_m) < 0.05: break
        return round((r_t + r_m) / 2, 2)

    def diagnosticar_con_prolog(self, score):
        nivel = list(prolog.query(f"nivel_riesgo({score}, Nivel)."))[0]['Nivel']
        tratamientos = list(prolog.query(f"protocolo({nivel}, L)."))[0]['L']
        return nivel, tratamientos

# ---------------------------
# Programa principal
# ---------------------------
if __name__ == "__main__":
    print("\nSistema MultiAgente SPTB-AI\n")
    with open("paciente_MGZ_001.json") as f:
        paciente = json.load(f)
    print(f"🧾 Paciente {paciente['patient_id']} ({paciente['fetal_sex']}) "
          f"– {paciente['gestational_age']} semanas\n")

    at, am, ac = AgenteTranscriptomico("AgenteTranscriptómico"), \
                 AgenteMetabolomico("AgenteMetabolómico"), \
                 AgenteClinico("AgenteClínico")
    coord = Coordinador([at, am, ac])

    resultados = coord.ejecutar(paciente)
    if coord.discrepancia(resultados):
        riesgo_final = coord.negociar_zeuthen(resultados)
    else:
        riesgo_final = round(sum(r["contenido"]["riesgo"] for r in resultados)/len(resultados), 2)
        print("\nSin discrepancias mayores, promedio aplicado.\n")

    nivel, protocolo = coord.diagnosticar_con_prolog(riesgo_final)

    print("---------------------------------------------------------")
    print("REPORTE FINAL DE DIAGNÓSTICO SPTB-AI")
    print("-----------------------------------------------------------")
    print(f"Riesgo calculado: {riesgo_final} → Nivel: {nivel.upper()}")
    print("Evidencias:")
    for r in resultados:
        print(f" - {r['emisor']}: {r['contenido']['evidencia']}")
    print("-----------------------------------------------------------")
    print("👩‍⚕️ Tratamiento recomendado por sistema experto:")
    for paso in protocolo:
        print(" →", paso)
    print("-----------------------------------------------------------\n")
