let table = document.createElement('table');
let thead = document.createElement('thead');
let tbody = document.createElement('tbody');

table.appendChild(thead);
table.appendChild(tbody);
document.getElementById('table1').appendChild(table);

// Adicionando conteúdo 

let row_2 = document.createElement('tr');
let row_2_data_1 = document.createElement('td1');
row_2_data_1.innerHTML = "NOME:";
row_2.appendChild(row_2_data_1);
tbody.appendChild(row_2);

let row_3 = document.createElement('tr');
let row_3_data_1 = document.createElement('td1');
row_3_data_1.innerHTML = "E-MAIL:";
row_3.appendChild(row_3_data_1);
tbody.appendChild(row_3);

let row_4 = document.createElement('tr');
let row_4_data_1 = document.createElement('td1');
row_4_data_1.innerHTML = "TELEFONE:";
row_4.appendChild(row_4_data_1);
tbody.appendChild(row_4);





