# SPTB-AI: Sistema Multi-Agente para Predicción de Parto Pretérmino Espontáneo

Proyecto final de la materia **Sistemas Multiagentes y Expertos**, desarrollado por **Priscila Inderkumer**.  
Integra tres agentes autónomos (Transcriptómico, Metabolómico y Clínico) para estimar el riesgo de **parto pretérmino espontáneo (SPTB)** y recomendar un protocolo de acción basado en reglas **Prolog**.

---

## Arquitectura

- **Python + Prolog (pyswip):** integración del razonamiento lógico con agentes inteligentes.  
- **Estrategia Zeuthen:** negociación multi-agente ante discrepancias de riesgo.  
- **Sistema experto clínico:** reglas médicas basadas en el trabajo original en Prolog.  
- **Visualización final:** diagrama de flujo de decisión clínica.

---

## Archivos incluidos

| Archivo | Descripción |
|----------|-------------|
| `sptb_ai_demo_v4.py` | Script principal del sistema multiagente |
| `reglas_sptb.pl` | Base de conocimiento Prolog con reglas clínicas |
| `paciente_MGZ_001.json` | Datos de ejemplo del paciente |
| `TPFinal_INDERKUMER_Priscila_v1.2.pdf` | Informe original completo |
| `README.md` | Documentación del proyecto |

---

## Ejecución

1. Instalar dependencias:
   ```bash
   sudo apt install swi-prolog graphviz
   pip install pyswip graphviz
