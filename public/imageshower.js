// get list of images
let xhr = new XMLHttpRequest();
xhr.open("GET", "images_lores/listofimages.json");
xhr.responseType = 'json';
xhr.send();

xhr.onload = function () {
    let imagenames = xhr.response;
    let imagecount = imagenames.length

    document.getElementById("imslider").max = imagecount - 1;
    document.getElementById("imslider").value = imagecount - 1;

    document.getElementById("imname").innerHTML = imagenames[imagecount - 1].slice(5, 20)
    document.getElementById("img").src = "images_lores/" + imagenames[imagecount - 1]
};

function showVal(newVal){
    if (xhr.readyState == 4){
        let imagenames = xhr.response;
        document.getElementById("imname").innerHTML = imagenames[newVal].slice(5, 20)
        document.getElementById("img").src = "images_lores/" + imagenames[newVal]
    }
}
