<!-- README.md generado por Nex Technology -->
<!-- Última modificación: 01/12/2025 -->

<h1 align="center">Sistema de Barbería</h1>
<p align="center"><em>(sistema de prueba para futura implementación)</em></p>

<p>
<strong>Descripción:</strong> Sistema de gestión para barbería con 3 niveles de acceso: <strong>barbero</strong>, <strong>administrador</strong> y <strong>recepcionista</strong>. Cada rol tiene funcionalidades diferenciadas (turnos/agenda, ventas, inventario, reportes básicos, administración de usuarios, etc.).  
</p>

<hr/>

<h2>Objetivo</h2>
<p>Proveer una base funcional y clara para una futura implementación productiva. Este repositorio contiene la estructura backend en <strong>Django</strong> y plantillas frontend basadas en <strong>HTML / Tailwind CSS</strong>, pensado para iterar sobre diseño y lógica por equipos.</p>

<hr/>

<h2>Recomendaciones para el equipo</h2>
<ul>
  <li>No utilizar IA como atajo: <strong>entender primero los conceptos</strong> antes de delegar en automatizaciones. (IA: útil, pero no reemplaza comprensión.)</li>
  <li>No tocar la rama <code>main</code>. Trabajar en ramas feature/ o abrir pull requests. </li>
  <li>Dividir funcionalidades y tareas a través de Trello. </li>
  <li>Consultar los diagramas (casos de uso, modelo entidad-relación) en Lucidchart para entender flujo y datos. </li>
  <li>Revisar y respetar el diseño de UI por nivel de acceso en Figma. </li>
  <li>Mantener comunicación asertiva y clara sobre la funcionalidad que se está desarrollando — preferiblemente por WhatsApp para coordinación rápida. </li>
  <li>Recomiendo consultar <a href="https://flowbite.com">Flowbite</a> para entender el contexto de funcionamiento de <strong>Tailwind CSS</strong> y componentes reutilizables.</li>
  <li>Recomiendo escribir variables y carpetas en snake case o lowercase y estrictamente en inglés.</li>
</ul>

<hr/>

<h2>Tecnologías utilizadas</h2>
<ul>
  <li><strong>Backend / Autenticación:</strong> Django</li>
  <li><strong>Frontend:</strong> HTML, CSS y Tailwind CSS</li>
  <li><strong>Íconos:</strong> FontAwesome</li>
  <li><strong>Fuente:</strong> Poppins (importada desde Google Fonts)</li>
  <li><strong>Base de datos:</strong> SQLite3 (configuración por defecto para desarrollo)</li>
</ul>

<hr/>

<h2>Futuras implementaciones (ideas / roadmap)</h2>
<ul>
  <li>Despliegue en vercel.</li>
  <li>Generación de reportes en PDF.</li>
  <li>Validación de suscripción: consultar Supabase para verificar si la barbería está solvente.</li>
  <li>Consulta de tasa del dólar (Banco Central de Venezuela) vía API o web-scraping.</li>
  <li>Migración/soporte para otra base de datos para ambientes productivos.</li>
  <li>Separar backend y frontend: implementación de SPA con React para la UI.</li>
</ul>

<hr/>

<h2>Instalación (desarrollo local)</h2>

<ol>
  <li><strong>Clona el repositorio</strong>
    <pre><code>git clone &lt;url-del-repositorio&gt;
cd &lt;nombre-del-proyecto&gt;</code></pre>
  </li>

  <li><strong>Crear entorno virtual y activar</strong>
    <pre><code>python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1</code></pre>
  </li>

  <li><strong>Instalar dependencias Python</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
    <small>Si no existe <code>requirements.txt</code>, instalar al menos Django: <code>pip install django </code></small>
  </li>

  <li><strong>Migraciones y base de datos</strong>
    <pre><code>python manage.py migrate
python manage.py createsuperuser  # crear admin para pruebas</code></pre>
  </li>

  <li><strong>Levantar servidor de desarrollo</strong>
    <pre><code>python manage.py runserver</code></pre>
    <p>Abrir <code>http://127.0.0.1:8000</code> en el navegador.</p>
  </li>
</ol>

<hr/>

<h2>Convenciones de Git</h2>
<ul>
  <li>No pushear directamente a <code>main</code>.</li>
  <li>Ramas: <code>feature/<nombre-funcionalidad></code>, <code>fix/<ticket></code>, <code>hotfix/*</code>.</li>
  <li>Cada PR debe tener descripción de la funcionalidad, screenshots (si aplica) y referencia al ítem en Trello.</li>
</ul>

<hr/>

<h2>Participantes (en representación de Nex Technology)</h2>
<ul>
  <li>Luis Alvarez</li>
  <li>Daniel Mata</li>
  <li>Alvaro Gutierrez</li>
</ul>

<hr/>

<h2>Licencia</h2>
<p>Por defecto MIT.</p>

<hr/>



<footer>
  <p><small>Última modificación: 01/12/2025</small></p>
</footer>


