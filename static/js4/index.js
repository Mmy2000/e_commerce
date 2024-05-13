const url = window.location.href
const searchForm = document.getElementById('searchForm')
const searchInput = document.getElementById('searchInput')
const results = document.getElementById('results')
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value

const sendData = (product)=>{
    $.ajax({
        type: "POST",
        url: 'result/',
        data: {
            'csrfmiddlewaretoken':csrf,
            'product':product
        },
        success:  (res)=> {
            console.log(res);
        },
        error:  (error)=>{
            console.log(error);
        }
    });
}

searchInput.addEventListener('keyup' , (e)=>{
    console.log(e.target.value);

    if (results.classList.contains('not-visible')) {
        results.classList.remove('not-visible')
    }
    sendData(e.target.value)
})