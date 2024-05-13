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
            console.log(res.data);
            const data = res.data
            if (Array.isArray(data)) {
                data.forEach(product=>{
                    results.innerHTML += `
                        <a href="${url}${product.slug}" class="text-decoration-none">
                            <div class="row mt-2 mb-2">
                                <div class="col-2">
                                    <img src="${product.image}" class="game-image" />
                                </div>
                                <div class="col-10">
                                    <h5>${product.name}</h5>
                                    <p class="text-muted">${product.price}</p>
                                </div>
                            </div>
                        </a>
                    `
                })
            }else{
                if (searchInput.value.length > 0) {
                    results.innerHTML = `<b>${data}</b>`
                }else{
                    results.classList.add('not-visible')
                }
            }
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