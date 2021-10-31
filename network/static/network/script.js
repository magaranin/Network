
function edit(post_id){
    const descriptionElement = document.querySelector(`#post_${post_id} .description`);
    const old_description = descriptionElement.innerText;
    //<textarea id="post_textarea" class="" value="${old_description}"></textarea>
    let textbox = document.createElement("textarea");
    textbox.value = old_description;
    textbox.id = "post_textarea";
    textbox.className = "";
    let submitButton = document.createElement("button");
    submitButton.innerHTML = "Save";
    submitButton.onclick = () => { 
        const new_description = document.querySelector('#post_textarea').value;
        updatePost(post_id, new_description);      
    }

    descriptionElement.innerHTML = '';
    descriptionElement.appendChild(textbox);
    descriptionElement.appendChild(submitButton);
    document.querySelectorAll('.edit_button').forEach(edit_button => edit_button.style.display = 'none');
    
}

function updatePost(post_id, new_description) {
    fetch(`/posts/${post_id}`, {
        method: "PUT",
        body: JSON.stringify({
            description: new_description
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
          }
        else {
            document.querySelector(`#post_${post_id} .description`).innerHTML = new_description;
        }
    })
    document.querySelectorAll('.edit_button').forEach(edit_button => edit_button.style.display = 'block');
}

function likeUnlike(post_id) {
    fetch(`/posts/${post_id}/like_unlike`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
        }
        else {
            let likeCountElement = document.querySelector(`#post_${post_id} .likeCount`);
            let countNumber = parseInt(likeCountElement.innerHTML)
            let likeUnlikeElement = document.querySelector(`#post_${post_id} .likeUnlikeText`)
            if (likeUnlikeElement.innerHTML === "Like") {
                likeCountElement.innerHTML = countNumber + 1; 
                likeUnlikeElement.innerHTML = "Unlike";
            }
            else {
                likeCountElement.innerHTML = countNumber - 1;
                likeUnlikeElement.innerHTML = "Like";
            }            
        }
    })
}   

