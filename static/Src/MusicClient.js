// Music player


const Socket = io();



Socket.on("connect", function(){
console.log("Connected succesfully");
});


Socket.on("GenericResponse",function(Data){ // For responses from the server

console.log("Server Message: " + Data["Status"])

});


Socket.on("SearchResults",function(Results){ // For getting results.

    console.log(JSON.stringify(Results))

});


function AddList(Text,Url){ //To do later.
    const ListItem = document.createElement("li")
    const ListSpan = document.createElement("span")

}



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



