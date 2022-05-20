let table = document.createElement('table');
let thead = document.createElement('thead');
let tbody = document.createElement('tbody');

table.appendChild(thead);
table.appendChild(tbody);


document.getElementById('table1').appendChild(table);




// Criando primeira 'fileira' da tabela, está sendo usada como titulo

// let row_1 = document.createElement('tr');
// let heading_1 = document.createElement('th');
// heading_1.innerHTML = "Lista de Cursos criados pelo Coordenador";
// row_1.appendChild(heading_1);
// thead.appendChild(row_1);

// Adicionando conteúdo 
for (let i=1; i<=5; i++)  {
	
    let row_2 = document.createElement('tr');
    let row_2_data_1 = document.createElement('td1');
    row_2_data_1.innerHTML = "CURSO";

    row_2.appendChild(row_2_data_1);
    tbody.appendChild(row_2);

}


//--------------------- 2º TABELA ------------------------------------


let table2 = document.createElement('table2');
let thead2 = document.createElement('thead2');
let tbody2 = document.createElement('tbody2');

table2.appendChild(thead2);
table2.appendChild(tbody2);


document.getElementById('table2').appendChild(table2);

// Criando primeira 'fileira' da tabela, está sendo usada como titulo
let t2_row_1 = document.createElement('tr');
let t2_heading_1 = document.createElement('th');
let t2_heading_2 = document.createElement('th');

t2_heading_1.innerHTML = "Curso";
t2_heading_2.innerHTML = "Disciplina";

t2_row_1.appendChild(t2_heading_1);
t2_row_1.appendChild(t2_heading_2);

thead2.appendChild(t2_row_1);

// Adicionando conteúdo 










