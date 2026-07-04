# Dimensión Zombi — Sitio oficial

Sitio estático (HTML/CSS/JS puro, sin dependencias de pago) para el canal de TikTok
**@dimensionzombiclubdehor**.

## Publicar gratis en GitHub Pages

1. Crea una cuenta gratuita en https://github.com si no tienes una.
2. Crea un repositorio nuevo. Puedes llamarlo, por ejemplo, `dimension-zombi-web`.
   Márcalo como **público** (los repos privados también sirven, pero en el plan
   gratuito Pages solo publica sitios de repos públicos).
3. Sube el archivo `index.html` de esta carpeta a la raíz del repositorio
   (botón "Add file" → "Upload files" en la web de GitHub, sin necesidad de usar
   la terminal).
4. Ve a **Settings → Pages** dentro del repositorio.
5. En "Branch", selecciona `main` (o `master`) y la carpeta `/root`, luego
   **Save**.
6. Espera 1–2 minutos. GitHub te dará una URL parecida a:
   `https://tu-usuario.github.io/dimension-zombi-web/`
   Esa es la página ya publicada, gratis, para siempre, sin anuncios.

## Activar el buzón de historias

Abre `index.html`, busca cerca del final la línea:

```js
const FORM_URL = "";
```

Pega ahí la URL de tu Google Form (instrucciones completas en el propio
archivo, en el comentario justo arriba de esa línea). Guarda el archivo y
vuelve a subirlo a GitHub (mismo botón "Upload files", GitHub lo detecta como
una actualización).

## Actualizar los videos más recientes

Busca en `index.html` la sección `<!-- TRANSMISIONES RECIENTES -->`. Cada
tarjeta tiene un bloque `tiktok-embed`. Para cada video nuevo:

1. Copia el enlace del video desde TikTok (botón compartir → copiar enlace).
2. Reemplaza el valor de `cite="..."` con ese enlace.
3. TikTok se encarga de renderizar el video automáticamente gracias al script
   `embed.js` que ya está incluido al final del archivo.

## Notas

- No necesitas comprar hosting ni dominio para tener el sitio en línea; el
  dominio `usuario.github.io` es gratis. Si más adelante quieren un dominio
  propio (ej. `dimensionzombi.com`), GitHub Pages también lo admite conectando
  un dominio comprado aparte (~$10–15 USD/año).
- El "Buzón de historias" usa Google Forms como backend gratuito: no requiere
  servidor propio ni base de datos.
