const tbody = document.querySelector('.table-body'); 

$('#searchField').on("keyup", function (e) {
    const searchValue = $(this).val()

    if (searchValue.length > 0) {
        console.log(searchValue);
        $('.pagination-container').addClass('d-none');
        tbody.innerHTML = "";
        fetch("/search/", {
            body: JSON.stringify({ searchText : searchValue}),
            method: "POST", 
            headers:{
                "Content-Type": "application/json"
            }, 
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data); 
            
            $('.app-table').addClass('d-none');
            $('.table-output').removeClass('d-none');


            if (data.length===0) {
                $('#no-results-style').removeClass('d-none');
                $('.table-output').addClass('d-none');
            } else {
                $('#no-results-style').addClass('d-none');
                data.forEach(item => {    
                    tbody.innerHTML +=      
                        `
                        <tr>
                        <td> ${item.amount} </td>
                        <td> ${item.category}</td>
                        <td> ${item.description} </td>
                        <td> ${item.date} </td>
                        </tr>`
                });
            }
        });
    } else {
        $('.app-table').removeClass('d-none');
        $('.pagination-container').removeClass('d-none');
        $('.table-output').addClass('d-none');
    }
});


