// script.js

document.getElementById('upload').addEventListener('change', handleFile, false);
document.getElementById('generate-chart').addEventListener('click', redirectToChartPage);

let jsonData = []; // Variable global para almacenar los datos

function handleFile(e) {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.onload = function(event) {
    const data = new Uint8Array(event.target.result);
    const workbook = XLSX.read(data, { type: 'array' });

    // Asumiendo que el primer sheet es el que nos interesa
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];

    // Convertir datos de Excel a JSON
    jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

    // Llamar a funciones para crear gráficos y tablas
    populateFilterOptions(jsonData[0]); // Usar la primera fila para las opciones de filtro
    createTable(jsonData);
  };

  reader.readAsArrayBuffer(file);
}

function populateFilterOptions(headers) {
  const columnFilter = document.getElementById('column-filter');
  const valueColumnFilter = document.getElementById('value-column-filter');
  const singleColumnFilter = document.getElementById('single-column-filter');

  // Limpiar opciones anteriores
  columnFilter.innerHTML = '';
  valueColumnFilter.innerHTML = '';
  singleColumnFilter.innerHTML = '';

  headers.forEach((header, index) => {
    const option = document.createElement('option');
    option.value = index; // Usamos el índice como valor
    option.text = header;
    columnFilter.appendChild(option);
    valueColumnFilter.appendChild(option.cloneNode(true)); // Clonar para agregar a ambos select
    singleColumnFilter.appendChild(option.cloneNode(true)); // Clonar para agregar a ambos select
  });
}

function redirectToChartPage() {
  const columnFilter = document.getElementById('column-filter');
  const valueColumnFilter = document.getElementById('value-column-filter');
  const singleColumnFilter = document.getElementById('single-column-filter');
  const chartType = document.getElementById('chart-type').value;

  const selectedLabelColumn = columnFilter.value;
  const selectedValueColumn = valueColumnFilter.value;
  const selectedSingleColumn = singleColumnFilter.value;

  if (selectedLabelColumn === selectedValueColumn) {
    alert('Las columnas de etiquetas y valores no pueden ser las mismas.');
    return;
  }

  // Guardar datos seleccionados en localStorage para que estén disponibles en la página de gráficos
  localStorage.setItem('jsonData', JSON.stringify(jsonData));
  localStorage.setItem('selectedLabelColumn', selectedLabelColumn);
  localStorage.setItem('selectedValueColumn', selectedValueColumn);
  localStorage.setItem('selectedSingleColumn', selectedSingleColumn);
  localStorage.setItem('chartType', chartType);

  // Redirigir a la página de gráficos
  window.location.href = 'charts.html';
}

function createTable(data) {
  const table = document.getElementById('data-table');

  // Limpiar contenido previo de la tabla
  table.innerHTML = '';

  // Crear cabecera de la tabla
  const header = document.createElement('thead');
  const headerRow = document.createElement('tr');
  data[0].forEach(col => {
    const th = document.createElement('th');
    th.innerText = col;
    headerRow.appendChild(th);
  });
  header.appendChild(headerRow);
  table.appendChild(header);

  // Crear cuerpo de la tabla
  const tbody = document.createElement('tbody');
  data.slice(1).forEach(row => {
    const tr = document.createElement('tr');
    row.forEach(cell => {
      const td = document.createElement('td');
      td.innerText = cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
}
function toggleMenu() {
    var menuContent = document.getElementById("menu-content");
    if (menuContent.style.display === "block") {
        menuContent.style.display = "none";
    } else {
        menuContent.style.display = "block";
    }
}

