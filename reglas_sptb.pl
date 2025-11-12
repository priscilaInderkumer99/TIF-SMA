% ------------------------------
% Base de conocimiento SPTB-AI
% ------------------------------

% Nivel de riesgo según score numérico
nivel_riesgo(RiskScore, alto) :- RiskScore >= 0.75.
nivel_riesgo(RiskScore, medio) :- RiskScore < 0.75, RiskScore >= 0.55.
nivel_riesgo(RiskScore, bajo) :- RiskScore < 0.55.

% Reglas de tratamiento asociadas a cada nivel
protocolo(alto, [
  hospitalizacion_inmediata,
  corticoides(betametasona, '12mg IM c/24h x2'),
  monitoreo_fetal(intensivo, 'c/4h'),
  tocoliticos(si_progresion),
  sulfato_magnesio(neuroproteccion)
]).

protocolo(medio, [
  control_obstetrico('en 24 horas'),
  reposo_domiciliario
]).

protocolo(bajo, [
  seguimiento_ambulatorio,
  control_rutinario
]).
