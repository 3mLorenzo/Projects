function token(name){
    const value = `: ${document.cookie}`;
    const parts = value.split(`: ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();

}

function submit(id) {

    const textarea = document.getElementById(`textarea_${id}`).value;
    const content = document.getElementById(`${id}_content`);
    const modal = document.getElementById(`modal_edit_post_${id}`);

    fetch(`edit/${id}`, {
        method:"POST",
        headers:{"content-type":"application/json", "X-CSRFToken":token("csrftoken")},
        body: JSON.stringify({
            content:textarea
        })
    })
    .then(response => response.json())
    .then(result => {

        content.innerHTML = result.data
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        // get modal backdrops
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        // remove every modal backdrop
        for(let i=0; i<modalsBackdrops.length; i++) {
        document.body.removeChild(modalsBackdrops[i]);
        }
    })
}

function like(id, liked) {

    const button = document.getElementById(`${id}`);
    button.classList.remove("fa-thumbs-down");
    button.classList.remove("fa-thumbs-up");

    if (liked.indexOf(id) >= 0) {
        var like = true;
    }
    else {
        var like = false;
    }

    if (like === true) {
        fetch(`r_like/${id}`)
        .then(response => response.json())
        .then(result => {
            button.classList.add("fa-thumbs-up");
        })
    }
    else {
        fetch(`a_like/${id}`)
        .then(response => response.json())
        .then(result => {
            button.classList.add("fa-thumbs-down");
        })
    }

    like = !like
}