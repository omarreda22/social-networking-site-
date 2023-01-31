const imageForm = document.getElementById("image-form");
const formCSRF = document.getElementsByName('csrfmiddlewaretoken');
const avatarInput = document.getElementById('id_avatar');
const DisplayNewAvatar = document.getElementById('display-new-avatar');

const newAvatarURL = document.getElementById('new-avatar-url');
const imageCloesForm = document.getElementById('image-form-close');

// Alert 
const alertBox = document.getElementById('alert-box')

const alert = function(statue, message){
    alertBox.innerHTML = `
    <div class="alert alert-${statue} alert-dismissible fade show mt-3 text-center" role="alert">
        ${message}.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close" id="close-alert">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    const closeAlert = document.getElementById("close-alert");
    setTimeout(()=>{
        closeAlert.click();
    }, 3000)
}


// Update Avatar

avatarInput.addEventListener('change', ()=>{
    const newAvatar = avatarInput.files[0];
    const newAvatarUrlCreate = URL.createObjectURL(newAvatar);
    DisplayNewAvatar.innerHTML = `<img src="${newAvatarUrlCreate}" width="100%" class="rounded-circle mt-5" width="170px">`;
});

url = '';

imageForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[0].value);
    form.append('avatar', avatarInput.files[0]);
    $.ajax({
        type: 'POST',
        url: 'update_image',
        enctype: 'multipart/form-data',
        data: form,
        success: function (response){
            const newAvatar = avatarInput.files[0];
            const newAvatarUrlCreate = URL.createObjectURL(newAvatar);
            newAvatarURL.src = newAvatarUrlCreate
            alert('success', 'Avatar Updated Successfully')
            imageCloesForm.click()
        },
        error: function(error){
            // console.log(error)
            imageCloesForm.click()
            alert('danger', 'Opp... data invalid')
        },        
        cache: false,
        contentType: false,
        processData: false,
    })
})


// Add ELert For Success
////////////////
// Update Bio
const bioForm = document.getElementById('bio-form');
const bio = document.getElementById('id_bio');
const bioUpdated = document.querySelector(".bio");
const closeBioForm = document.getElementById('bio-close-form');

bioForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[1].value);
    form.append('bio', bio.value);

    $.ajax({
        type: 'POST',
        url: 'update_bio',
        data: form,
        success: function(response){
            bioUpdated.innerHTML = `<p>${response.bio}</p>`
            closeBioForm.click()
            alert('success', 'Bio Updated Successfully')
        },
        error: function(error){
            closeBioForm.click()
            alert('danger', 'Opp... data invalid')},
        cache: false,
        contentType: false,
        processData: false,
    })
})

/////////////////////////////////////////////////////////

// Myprofile Information
const infoForm = document.getElementById('information-form');
const username = document.getElementById('id_username');
const firstname = document.getElementById('id_first_name');
const lastname = document.getElementById('id_last_name');
const country = document.getElementById('id_country');
const gender = document.getElementById('id_gender');
const year = document.getElementById('id_date_of_birth_year');
const month = document.getElementById('id_date_of_birth_month');
const day = document.getElementById('id_date_of_birth_day');

const firstname_ = document.getElementById('first-name');
const lastname_ = document.getElementById('last-name');
const country_ = document.getElementById('country');
const gender_ = document.getElementById('gender');
const dataOfBirth = document.getElementById('date-of-birth');

const btnCloseInfoForm = document.getElementById('info-close-form')

infoForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[2].value);
    form.append('username', username.value);
    form.append('first_name', firstname.value);
    form.append('last_name', lastname.value);
    form.append('country', country.value);
    form.append('gender', gender.value);
    form.append('date_of_birth_year', year.value);
    form.append('date_of_birth_month', month.value);
    form.append('date_of_birth_day', day.value);

    

    $.ajax({
        type: 'POST',
        url: '',
        data: form,
        success: function(response){
            if (response.infoError.username){    
                alert('danger', response.infoError.username);
                const closeAlert = document.getElementById("close-alert");
                setTimeout(()=>{
                    closeAlert.click();
                }, 3000)
            };
            firstname_.innerHTML = response.first_name
            lastname_.innerHTML = response.last_name
            country_.innerHTML = response.country
            gender_.innerHTML = response.gender
            dataOfBirth.innerHTML = response.date

            btnCloseInfoForm.click();
            alert('success', 'Information Updated Successfully')
        },
        error: function(error){
            btnCloseInfoForm.click();
            alert('danger', 'Opp... data invalid')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

// Display Error in page if Exists




////////////////////////////////////////////////////////////////////////////////////////

// add new post

const addNewPostForm = document.getElementById('add-new-post');
const imageId = document.getElementById('id_image');
const contentNewPost = document.getElementById('id_content');

const openNewImagePost = document.querySelector('.open_new_image_post')

const newPostAdder = document.getElementById('all-posts');
const postCount = document.getElementById('posts-count');
const addNewPostCloseForm = document.querySelector('.new-post-close-form');

imageId.addEventListener('change', ()=>{
    const loadUrl = imageId.files[0];
    const urlNewPost = URL.createObjectURL(loadUrl) 
    openNewImagePost.innerHTML =  `<img src="${urlNewPost}" width="50%" width="170px">`;
})


addNewPostForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[0].value);
    form.append('image', imageId.files[0]);
    form.append('content', contentNewPost.value);

    $.ajax({
        type:'POST',
        url: '/posts/new_post/',
        enctype: 'multipart/form-data',
        data:form,
        success: function(response){
            const newPostHTML = `
            <div class="card myprofile-post mb-3">
                <div class="card-header">
                    <img src="${response.user_image}" class="rounded-circle" style="width:45px"alt="Avatar" />
                    <span  class='username-phr ml-2 profile-username'>${response.user_username}</span>
                    <span class="tect-muted" style='float:right; margin-top:10px'>
                        Just Now
                    </span>
                </div>
                <div class="card-body text-center">
                    <h5 class="card-title text-left mb-4 mt-2">${response.content}</h5>
                    <img src="${response.image}" style="width:50%" class="card-img-top" alt="...">
                </div>
                <div class="card-footer text-muted text-center">
                    <h5>
                        <a href="" style="color:#6C7587" data-toggle="modal" data-target="#profileLikesPeople-${response.post_id}">Likes(0)</a>, 
                        <a href="" style="color:#6C7587" data-toggle="modal" data-target="#profileCommentsPeople-${response.post_id}">Comments(0)</h5></a>
                </div>
            </div>
            `;
            newPostAdder.insertAdjacentHTML('afterbegin', newPostHTML);
            const numberPosts = Number(postCount.textContent) + 1 ;
            postCount.innerHTML = numberPosts;
            alert('success', 'New Post Added');
            contentNewPost.value = '';
            imageId.value = '';
            openNewImagePost.innerHTML = '';
            addNewPostCloseForm.click();
            // imageId.value = '';
        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

///////////////////////////////////////////////////////////////////////////////////

const editPostForm = document.querySelectorAll('.edit-post-form');
// console.log(editPostForm)

for(let i = 0; i<editPostForm.length; i++){
    editPostForm[i].addEventListener('submit', (e)=>{
        e.preventDefault();
        
        const postId = editPostForm[i].classList[1]
        const content = document.getElementById(`edit-post-content-${postId}`);
        const imageField = document.getElementById(`edit-post-image-${postId}`);
        // const imageField = document.getElementById(`edit-post-image-${postId}`).files[0];
        // console.log(content.value)
        // console.log(image.files[0])
        const imageEditHTML = document.getElementById(`edit-image-${postId}`);
        // console.log(imageEditHTML)
        if(imageField.files[0]){
            const newImageUrl = URL.createObjectURL(imageField.files[0]);
            
            imageEditHTML.innerHTML = `<img src="${newImageUrl}" style="width:50%" class="card-img-top"  alt="...">`
        }
        
        // imageField.addEventListener('change', ()=>{
        //     console.log('ina')
        // })
        const form = new FormData();
        form.append('csrfmiddlewaretoken', formCSRF[0].value);
        form.append('content', content.value);
        form.append('image', imageField.files[0]);
        // if(imageField.files[0]){
        //     console.log(imageField.files[0])
        // }
        // console.log(form.)
        
        const generalPost = document.getElementById(`general-${postId}`);
        const closeBtn = document.getElementById(`edit-post-close-${postId}`);
        $.ajax({
            type:'POST',
            url: `/myprofile/update_post/${postId}/`,
            enctype: 'multipart/form-data',
            data:form,
            success: function(rep){
                generalPost.innerHTML = `
                    <h5 class="card-title text-left mb-4 mt-2">${rep.content}</h5>
                    <img src="${rep.image}" style="width:50%" class="card-img-top" alt="...">
                `;
                alert('success', 'Post Updated')
                closeBtn.click();
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    })
}

//////////////////////////////////////////////////////////////////////////////////////////

// delete post 


const deletePostForm = document.querySelectorAll('.delete-post-form');

for(let i = 0; i<deletePostForm.length; i++){
    deletePostForm[i].addEventListener('submit', (e)=>{
        e.preventDefault();
        const postId = deletePostForm[i].classList[1];

        const form = new FormData();
        form.append('csrfmiddlewaretoken', formCSRF[0].value);
        form.append('id', postId);

        const generalPost = document.getElementById(`post-post-${postId}`);
        const closeDelete = document.getElementById(`delete-post-close-${postId}`);
        $.ajax({
            type: 'POST',
            url: `/myprofile/delete_post/${postId}/`,
            data: form,
            success: function(rep){
                alert('success', 'Post Deleted')
                closeDelete.click();
                generalPost.remove();
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,

        })
    })
}