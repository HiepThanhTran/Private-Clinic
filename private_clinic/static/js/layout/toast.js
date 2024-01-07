/* _______________________
Command use toast message:

toast({
	title: "Your title!",
	message: "Your message.",
	type: "Your type you want",
	duration: "Duration for animation",
	durationDelay: "Duration delay for animation".
});
_______________________*/

const icons = {
    info: 'fa-solid fa-circle-info',
    success: 'fa-solid fa-circle-check',
    error: 'fa-solid fa-circle-exclamation',
    warning: 'fa-solid fa-circle-exclamation',
};

const toastID = document.createElement('div');
toastID.id = 'toastId';
document.body.prepend(toastID);

function toast({title, message, type, duration = 2000, durationDelay = 3000}) {
    const toast = document.createElement('div');

    let autoRemove = setTimeout(function () {
        toastID.removeChild(toast);
    }, duration + durationDelay);

    toast.onclick = function (e) {
        if (e.target.closest('.my_toast__close')) {
            toastID.removeChild(toast);
            clearTimeout(autoRemove);
        }
    };

    toast.classList.add('my_toast', `my_toast--${type}`);
    const animationDuration = (duration / 1000).toFixed(2);
    const animationDelay = (durationDelay / 1000).toFixed(2);
    toast.style.animation = `showToast ease 0.3s, hiddenToast linear ${animationDuration}s ${animationDelay}s forwards`;
    toast.innerHTML = `<div class="my_toast__icon"><i class="${icons[type]}"></i></div>
                        <div class="my_toast__body">
                            <h3 class="my_toast__title">${title}</h3>
                            <div class="my_toast__msg">${message}</div>
                        </div>
                        <div class="my_toast__close"><i class="fa-solid fa-xmark"></i></div>`;
    toastID.appendChild(toast);


    toast.addEventListener('mouseenter', () => {
        clearTimeout(autoRemove);
        toast.style.animation = null;
    });

    toast.addEventListener('mouseleave', () => {
        autoRemove = setTimeout(() => {
            toastID.removeChild(toast);
        }, duration + durationDelay);
        toast.style.animation = `showToast ease 0.3s, hiddenToast linear ${animationDuration}s ${animationDelay}s forwards`;
    });
}