// Music player


const Socket = io();



Socket.on("connect", function(){
console.log("Connected succesfully");
});


Socket.on("GenericResponse",function(Data){

console.log("Server Message: " + Data["Status"])

});



document.addEventListener("keydown",function(Event){ // Press enter to search song
    if (Event.key === "Enter") {
        Event.preventDefault(); // Prevent it from activating when typing and stuff
        OnSubmit();
    }
});


function OnSubmit(){

    var MusicInput = document.getElementById("MusicSearch"); // Get all the useful elements.


    var RequestData = {
        RequestType: "SearchSongs", // Request type
        Search: MusicInput.value // Search
    };


    Socket.emit("ClientSubmit",RequestData)


}



