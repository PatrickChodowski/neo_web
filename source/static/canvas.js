window.addEventListener("load",  () => {
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");

    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth-400;

    ctx.fillRect(500,500,50,50);
});