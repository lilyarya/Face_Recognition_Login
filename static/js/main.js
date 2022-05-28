let video = document.getElementById("video");   // Initializing used elements;
let canvas = document.getElementById("myCanvas");
let ctx = canvas.getContext('2d');
let urlInput = document.getElementById("url");
let labels = document.getElementsByTagName('label');
let emailInput = document.getElementById("email");
let submitInput = document.getElementById("submit");

submitInput.onclick = login;  //onlick event on the button
urlInput.value = ""; 
urlInput.setAttribute("accept", "image/png");
labels[1].hidden = "hidden";
emailInput.setAttribute("placeholder", "User ID");
urlInput.setAttribute("placeholder", "URL");

urlInput.hidden = "hidden"

var localMediaStream = null;
var constraints = {
    video: {
        width: { max: 1280 },        //styles on video (max is used for varying screen size);
        height: { max: 720 }
    },
    audio: false
};

navigator.mediaDevices.getUserMedia(constraints)  
    .then(function(stream) {   //upon execution of above this has to be performed (like a promise).
        video.srcObject = stream;
        localMediaStream = stream;
    })
    .catch(function(error) {   //handling error
        console.log(error);
    });

function login() {   //our login fuction.
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);  //for facial recognition login access.
    var dataURL = canvas.toDataURL('image/png');
    document.getElementById("url").value = dataURL;
}  