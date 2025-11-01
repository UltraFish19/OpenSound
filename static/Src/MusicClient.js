// Music player


const Socket = io();
let SearchingFor = "" // What client is searching for

let SongNameLabel;
let PlayButton;
let MusicProgressBar;



document.addEventListener("DOMContentLoaded", function() { //Wait for DOM to load

    SongNameLabel = document.getElementById("SongName");
    PlayButton = document.getElementById("PlayButton");
    MusicProgressBar = document.getElementById("MusicProgressBar");

    MusicProgressBar.value = 0
});

const PlayButtonTexts = {"true" : "Pause","false" : "Play"}
let UserDragging = false; // If the user is dragging or not




//--------------------------------<Websockets>-------------------------------------------

Socket.on("connect", function(){
console.log("Connected succesfully");
});


Socket.on("GenericResponse",function(Data){ // For responses from the server

console.log("Server Message: " + Data["Status"])

});


Socket.on("SearchResults",function(Data){ // For getting results.



    Result = Data["Result"]
    Details = Data["Details"]



       if (Details["RemovePreviousResults"] === true){
        ClearResultsList()
       }

        AddResultsList(Result["Name"] + " by " + Result["Author"], Result["Url"])



});


Socket.on("ServerDetails",function(Data){
MusicDetails = Data["Music"]

 SongNameLabel.textContent = "Playing " + MusicDetails["Name"]
 PlayButton.textContent = PlayButtonTexts[MusicDetails["IsPlaying"]] // Add the proper text for if it is paused or playing
 
 let TimePosition = MusicDetails["TimePosition"]
 let Duration = MusicDetails["TimeLength"]


 if (UserDragging == true) {
 let MusicProgressBarValue = (TimePosition / Duration) * 1000
 MusicProgressBar.value = MusicProgressBarValue

 }


});


//--------------------------------<Event Listeners>-------------------------------------------


MusicProgressBar.addEventListener("mousedown",() =>{
UserDragging = true
});

MusicProgressBar.addEventListener("touchstart",() =>{
UserDragging = true
});

MusicProgressBar.addEventListener("mouseup",() =>{
UserDragging = false
});

MusicProgressBar.addEventListener("touchend",() =>{
UserDragging = false
});


//--------------------------------<Functions>-------------------------------------------
function ClearResultsList(){
document.getElementById("SearchResultsContainer").innerHTML = ""
};

function PlaySong(Url){
    Socket.emit(

        "ClientSubmit",
        {
            RequestType : "PlaySong",
            Search : Url
        }


    )
}


function AddResultsList(Text,Url){ //To do later.
    const ListContainer = document.getElementById("SearchResultsContainer")
    const ListItem = document.createElement("li")
    const ListButton = document.createElement("Button")

    ListButton.textContent = Text
    ListButton.className = "SearchResultsList"
    ListButton.id = Url // Store The url as the ID
    ListButton.onclick = function(){
        PlaySong(this.id)
    }

    ListItem.appendChild(ListButton)

    ListContainer.appendChild(ListItem)
    

}


function DisablePlayingFeatures(To){} // Disable or Enable play button and everything else


document.addEventListener("keydown",function(Event){ // Press enter to search song
    if (Event.key === "Enter") {
        Event.preventDefault(); // Prevent it from activating when typing and stuff
        OnSubmit();
    }
});


function ToggleSongPlaying(){ //Pause and play music.
Socket.emit("ClientSubmit",{
    RequestType : "PauseSong",
    Search: "Uhh hi?"

});
};

function OnSubmit(){

    var MusicInput = document.getElementById("MusicSearch"); // Get all the useful elements.
    ClearResultsList()

    SearchingFor = MusicInput.value

    var RequestData = {
        RequestType: "SearchSongs", // Request type
        Search: MusicInput.value // Search
    };


    Socket.emit("ClientSubmit",RequestData)


}



