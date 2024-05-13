const url = window.location.href
const searchForm = document.getElementById('searchForm')
const searchInput = document.getElementById('searchInput')
const results = document.getElementById('results')
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value

searchInput.addEventListener('keyup' , (e)=>{
    console.log(e.target.value);

    if (results.classList.contains('not-visible')) {
        results.classList.remove('not-visible')
    }
})