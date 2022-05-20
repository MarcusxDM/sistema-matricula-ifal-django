let table = document.createElement('table');
let thead = document.createElement('thead');
let tbody = document.createElement('tbody');

table.appendChild(thead);
table.appendChild(tbody);


document.getElementById('table1').appendChild(table);



let row_1 = document.createElement('tr');
let heading_1 = document.createElement('th');
heading_1.innerHTML = "Professores";
row_1.appendChild(heading_1);
thead.appendChild(row_1);

// Adicionando conteúdo 
for (let i=1; i<=5; i++)  {
	
    let row_2 = document.createElement('tr');
    let row_2_data_1 = document.createElement('td');
    row_2_data_1.innerHTML = "Professor" +i;

    row_2.appendChild(row_2_data_1);
    tbody.appendChild(row_2);

}












