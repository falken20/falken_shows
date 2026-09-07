# Estimación de coste para uso personal

Este documento estima el coste orientativo de los servicios necesarios para ejecutar esta aplicación con uso personal, considerando aproximadamente 10–15 shows al año y una precarga de 15 años.

## Supuesto base

- 10–15 shows al año
- precarga estimada: 150–225 shows
- uso personal, no masivo
- una base de datos pequeña
- frontend y backend desplegados en Cloud Run
- almacenamiento limitado de fotos, archivos o documentos

## Resultado estimado

### Escenario mínimo

- Cloud SQL: 15–20 €/mes
- Cloud Run: 0–5 €/mes
- Cloud Storage: 1–3 €/mes
- Secret Manager + Artifact Registry: 2–5 €/mes
- Logs / Monitoring: 1–3 €/mes
- Total: 20–35 €/mes
- Total anual: 240–420 €/año

### Escenario recomendable

- Cloud SQL: 20–30 €/mes
- Cloud Run: 2–8 €/mes
- Cloud Storage: 2–5 €/mes
- Secret Manager + Artifact Registry: 3–6 €/mes
- Logs / Monitoring: 2–5 €/mes
- Total: 30–60 €/mes
- Total anual: 360–720 €/año

## Estimación recomendada para tu caso

Para tu uso personal, la cifra más razonable sería:

- 40–60 €/mes
- 480–720 €/año

## Desglose por servicio

### Cloud SQL (PostgreSQL)

Es el servicio que más suele influir en el precio.

- Instancia pequeña: 15–30 €/mes
- Con almacenamiento extra o backups: 20–40 €/mes

Para un proyecto personal con 150–225 shows, una instancia pequeña es suficiente.

### Cloud Run

Se usa para desplegar backend y frontend con tráfico muy bajo.

- Coste estimado: 0–10 €/mes
- Normalmente muy bajo si no hay mucho tráfico

### Cloud Storage

Para guardar fotos, archivos o backups pequeños.

- Coste estimado: 1–5 €/mes
- Si guardas mucho contenido multimedia puede crecer ligeramente

### Secret Manager

Para almacenar secretos como claves JWT o credenciales.

- Coste estimado: 0,5–2 €/mes

### Artifact Registry

Para guardar imágenes Docker.

- Coste estimado: 1–5 €/mes

### Cloud Build

Para compilar y desplegar automáticamente.

- Coste estimado: 0–5 €/mes

### Cloud Logging / Monitoring

Para registros y observabilidad.

- Coste estimado: 1–5 €/mes

## Conclusión

Para un uso personal con 10–15 shows al año y una base histórica de 15 años:

- la solución no debería ser cara
- el rango más realista es de 30–60 €/mes
- el coste total anual suele estar alrededor de 360–720 €/año

Esto es razonable para un proyecto personal bien mantenido y sin tráfico masivo.

## Recomendación concreta de Cloud SQL para tu caso

Para tu uso personal, la opción más barata y razonable es una instancia pequeña de PostgreSQL en Cloud SQL.

### Configuración recomendada
- Tipo: Cloud SQL for PostgreSQL
- Tamaño: instancia pequeña
- Almacenamiento: 10–20 GB
- Acceso: privado o restringido
- IP pública: no
- Backups: mínimos y automáticos
- Replica / HA: no, por ahora

### Por qué esta configuración encaja bien
- 150–225 shows no requieren una base de datos grande.
- El uso es personal y no masivo.
- Con una instancia pequeña tendrás suficiente capacidad para gestionar conciertos, artistas, ciudades, setlists y notas.
- Mantiene el coste bajo y evita gastos innecesarios.

### Coste esperado
- 15–30 €/mes aprox.

### Configuración mínima viable
Si quieres ir aún más barato:
- instancia pequeña
- 10 GB de almacenamiento
- backups mínimos
- acceso privado
- sin servicios extra

Esto puede quedar en torno a 10–20 €/mes, pero para un uso más estable durante años, yo me quedaría con la recomendación anterior (15–30 €/mes).

## Recomendaciones para reducir costes

Si quieres mantener el servicio lo más barato posible sin perder funcionalidad, estas son las mejores decisiones:

### 1) Usar una instancia pequeña de Cloud SQL
- No hace falta una base de datos grande.
- Con 150–225 shows y uso personal, una instancia pequeña es más que suficiente.
- Este punto suele ahorrar la mayor parte del presupuesto.

### 2) Mantener Cloud Run en modo mínimo
- Deja el backend y el frontend con un mínimo de recursos.
- Evita cambiar a configuraciones más grandes si no hay tráfico real.
- Para un uso personal, el coste de ejecución es normalmente bajo, pero conviene mantenerlo ajustado.

### 3) Guardar solo lo necesario en Cloud Storage
- Evita almacenar grandes archivos innecesarios.
- Si puedes, guarda imágenes comprimidas y solo lo esencial.
- Limita copias de seguridad redundantes.

### 4) Desactivar o reducir logs innecesarios
- Los logs se acumulan y pueden aumentar el coste.
- Mantén niveles de logging razonables.
- Revisa si hay errores repetidos o trazas demasiado verbosas.

### 5) Reutilizar infraestructura y no crear servicios extra
- No añadas servicios que no necesites para empezar.
- En este caso, con un uso personal, lo mejor es centrarse en Cloud Run + Cloud SQL + Secret Manager + Storage.

### 6) Configurar backups solo de forma sensata
- Los backups son útiles, pero no hace falta una política agresiva si el dato no es crítico.
- Haz copias de seguridad periódicas, pero no excesivas.

### 7) Mantener la app ligera
- Menos complejidad = menos costes operativos.
- Evita añadir demasiadas features o servicios periféricos que no vayas a usar.

### 8) Revisar el coste cada 3–6 meses
- Con uso real, podrás ver si una instancia o un servicio es innecesario.
- Normalmente, al principio se puede dejar todo mínimo y escalar solo si hace falta.

## Conclusión final

Para tu caso personal, la estrategia más económica es:

- Cloud SQL pequeña de PostgreSQL
- Cloud Run con recursos mínimos
- Storage solo para archivos necesarios
- logs y backups controlados
- sin servicios extras ni replicas por ahora

Con esta configuración, la recomendación más útil para ti es:

- 15–30 €/mes para la base de datos
- 30–60 €/mes en total para la infraestructura completa

Es decir, el proyecto sigue siendo muy económico para un uso personal y con una precarga de 15 años.
