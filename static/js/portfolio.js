document.addEventListener("DOMContentLoaded", function () {
        const modal = document.querySelector("#modalWin");
        const modalImg = modal.querySelector(".modal-window img");
        const galleryLinks = Array.from(document.querySelectorAll(".gallery a"));
        const nextBtn = modal.querySelector(".modal-next");
        const prevBtn = modal.querySelector(".modal-prev");

        let currentIndex = 0;

        function showImage(index) {
            const img = galleryLinks[index].querySelector("img");
            if (img) {
                modalImg.src = img.src;
                currentIndex = index;
            }
        }

        galleryLinks.forEach((link, index) => {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                showImage(index);
            });
        });

        nextBtn.addEventListener("click", function () {
            let nextIndex = (currentIndex + 1) % galleryLinks.length;
            showImage(nextIndex);
        });

        prevBtn.addEventListener("click", function () {
            let prevIndex = (currentIndex - 1 + galleryLinks.length) % galleryLinks.length;
            showImage(prevIndex);
        });
    });