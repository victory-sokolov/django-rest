const likeButton = document.querySelector('a.like-button');

likeButton.onclick = (e) => {
    likeButton.classList.toggle('liked');

    setTimeout(() => {
        e.target.removeClass('liked');
    }, 1000);
};
