

window.addEventListener('DOMContentLoaded', event => {
     Simple-DataTables
     https://github.com/fiduswriter/Simple-DataTables/wiki


    const datatablesSimple = document.getElementById('datatablesSimple');

    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});


//let myTable = document.querySelector("#myTable");
//let dataTable = new DataTable(myTable);
//
//
//let dataTable = new DataTable("#myTable", {
//    searchable: false,
//    fixedHeight: true,
//    ...
//});



