#!/usr/bin/env python3
"""
Actualiza datos/uv.json con el índice UV para Huachipato Terminal Portuario.

Fuentes:
  1. Pronóstico (siempre): Open-Meteo, modelo CAMS, para Bahía San Vicente.
     Entrega índice UV máximo de hoy, los próximos 7 días y la curva horaria.
  2. Medición oficial (opcional): Dirección Meteorológica de Chile, servicio
     getRecienteUvb de la Red Nacional de radiación UV. Requiere los secretos
     DMC_USUARIO y DMC_TOKEN en GitHub (Settings → Secrets → Actions).
     Se usa la estación de la red más cercana al terminal.

El índice publicado del día es el MAYOR entre el pronóstico y lo medido por la DMC
(criterio conservador para la protección de los trabajadores).
Solo usa la biblioteca estándar de Python.
"""
import json, math, os, sys, urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

LAT, LON = -36.732, -73.128
TZ = ZoneInfo("America/Santiago")
SALIDA = os.path.join(os.path.dirname(__file__), "..", "datos", "uv.json")
OM = os.environ.get("OPENMETEO_URL", "https://api.open-meteo.com/v1/forecast")
DMC = os.environ.get("DMC_URL", "https://climatologia.meteochile.gob.cl/application/servicios/getRecienteUvb")


def leer_json(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "HTP-Tablero-UV/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def pronostico():
    url = (f"{OM}?latitude={LAT}&longitude={LON}&daily=uv_index_max"
           f"&hourly=uv_index&timezone=America%2FSantiago&forecast_days=7")
    j = leer_json(url)
    dias = [{"fecha": f, "iuv": round(v, 1) if v is not None else None}
            for f, v in zip(j["daily"]["time"], j["daily"]["uv_index_max"])]
    horas = {}
    for t, v in zip(j["hourly"]["time"], j["hourly"]["uv_index"]):
        horas.setdefault(t[:10], []).append({"h": int(t[11:13]), "iuv": round(v or 0, 1)})
    return dias, horas


def distancia(lat1, lon1, lat2, lon2):
    r = math.radians
    a = (math.sin(r(lat2 - lat1) / 2) ** 2 +
         math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(r(lon2 - lon1) / 2) ** 2)
    return 6371 * 2 * math.asin(math.sqrt(a))


def medicion_dmc(hoy):
    usuario, token = os.environ.get("DMC_USUARIO"), os.environ.get("DMC_TOKEN")
    if not usuario or not token:
        return None
    j = leer_json(f"{DMC}?usuario={urllib.request.quote(usuario)}&token={urllib.request.quote(token)}")
    estaciones = j.get("datosRecientes") or []
    mejor = None
    for e in estaciones:
        est = e.get("estacion", {})
        try:
            d = distancia(LAT, LON, float(est["latitud"]), float(est["longitud"]))
        except (KeyError, TypeError, ValueError):
            continue
        if mejor is None or d < mejor[0]:
            mejor = (d, est, e.get("indiceUV") or [])
    if not mejor:
        return None
    dist, est, datos = mejor
    puntos = []
    for p in datos:
        try:
            # fecha/hora vienen en UTC: DD-MM-YYYY y HH:MM:SS
            t = datetime.strptime(f'{p["fecha"]} {p.get("hora", "00:00:00")}', "%d-%m-%Y %H:%M:%S")
            t = t.replace(tzinfo=timezone.utc).astimezone(TZ)
            v = float(str(p["indiceUV"]).replace(",", "."))
        except (KeyError, ValueError, TypeError):
            continue
        if t.date().isoformat() == hoy:
            puntos.append((t, v))
    if not puntos:
        return {"estacion": est.get("nombreEstacion", "").strip(), "distanciaKm": round(dist, 1), "maximo": None}
    puntos.sort()
    tmax, vmax = max(puntos, key=lambda x: x[1])
    tult, vult = puntos[-1]
    return {
        "estacion": est.get("nombreEstacion", "").strip(),
        "codigoNacional": est.get("codigoNacional"),
        "distanciaKm": round(dist, 1),
        "maximo": round(vmax, 1), "horaMaximo": tmax.strftime("%H:%M"),
        "ultimo": round(vult, 1), "horaUltimo": tult.strftime("%H:%M"),
    }


def main():
    ahora = datetime.now(TZ)
    hoy = ahora.date().isoformat()
    previo = {}
    try:
        with open(SALIDA, encoding="utf-8") as f:
            previo = json.load(f)
    except (OSError, ValueError):
        pass

    salida = {"generado": ahora.isoformat(timespec="minutes"), "fecha": hoy,
              "lugar": "Bahía San Vicente, Talcahuano", "lat": LAT, "lon": LON}
    errores = []
    try:
        dias, horas = pronostico()
        salida["pronostico"] = dias
        salida["horario"] = horas.get(hoy, [])
        salida["fuentePronostico"] = "Open-Meteo (modelo CAMS)"
    except Exception as e:  # mantiene el último pronóstico válido
        errores.append(f"pronóstico: {e}")
        for k in ("pronostico", "horario", "fuentePronostico"):
            if k in previo:
                salida[k] = previo[k]
    try:
        dmc = medicion_dmc(hoy)
        if dmc:
            salida["dmc"] = dmc
    except Exception as e:
        errores.append(f"DMC: {e}")
        if previo.get("fecha") == hoy and "dmc" in previo:
            salida["dmc"] = previo["dmc"]

    pron_hoy = next((d["iuv"] for d in salida.get("pronostico", []) if d["fecha"] == hoy), None)
    med = (salida.get("dmc") or {}).get("maximo")
    candidatos = [v for v in (pron_hoy, med) if v is not None]
    salida["iuvDia"] = round(max(candidatos)) if candidatos else None
    salida["origenIuv"] = ("dmc" if med is not None and (pron_hoy is None or med >= pron_hoy) else "pronostico") if candidatos else None

    h = salida.get("horario", [])
    umbral = 6 if any(x["iuv"] >= 6 for x in h) else 3
    altos = [x["h"] for x in h if x["iuv"] >= umbral]
    if altos:
        salida["horaMayor"] = f"{min(altos):02d}:00 – {max(altos) + 1:02d}:00"
    if errores:
        salida["avisos"] = errores

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: salida.get(k) for k in ("fecha", "iuvDia", "origenIuv", "horaMayor", "dmc", "avisos")}, ensure_ascii=False))
    if "pronostico" not in salida and "dmc" not in salida:
        sys.exit(1)


if __name__ == "__main__":
    main()
