// Music player


const Socket = io(); //The websocket
let CurrentUrl = ""

let SongNameLabel;
let PlayButton;
let MusicProgressBar;
let Duration;

let FavouriteImg;

let MusicDurationLabel;

//--------------------------------<Event Listeners>-------------------------------------------

document.addEventListener("DOMContentLoaded", function() { //Wait for DOM to load

    SongNameLabel = document.getElementById("SongName");
    PlayButton = document.getElementById("PlayButton");
    MusicProgressBar = document.getElementById("MusicProgressBar");
    FavouriteImg = document.getElementById("FavImg")
    MusicProgressBar.value = 0
    MusicDurationLabel = document.getElementById("MusicDurationLabel")


MusicProgressBar.addEventListener("change", () => {
    const Percentage = parseInt(MusicProgressBar.value) / 1000;
    const NewTime = Percentage * Duration;
    
    SetDuration(NewTime);
    UserDragging = false;
});

MusicProgressBar.addEventListener("mousedown", () => { UserDragging = true; });
MusicProgressBar.addEventListener("touchstart", () => { UserDragging = true; });


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


Socket.on("ServerDetails",function(Data){ // Data from server every 0.2 secs.
MusicDetails = Data["Music"];


 var SongName = MusicDetails["Name"]

 if (SongName == "" ) { // Nothing is playinh
    SongNameLabel.textContent = "Nothing is playing";

 } else if (MusicDetails["SongLoaded"] == false) { // Something is playing but it is loading
    SongNameLabel.textContent  = `Loading ${SongName}` // Javascript F-String
 } else {
    SongNameLabel.textContent  = `Playing ${SongName}`
 }

 PlayButton.textContent = PlayButtonTexts[MusicDetails["IsPlaying"]] // Add the proper text for if it is paused or playing
 
 let TimePosition = MusicDetails["TimePosition"];
 Duration = MusicDetails["TimeLength"];

 CurrentUrl = MusicDetails["CurrentUrl"];

 MusicDurationLabel.textContent = FormatTime(TimePosition) + "/" + FormatTime(Duration)

 if (UserDragging == false) {
 let MusicProgressBarValue = (TimePosition / Duration) * 1000;
 MusicProgressBar.value = MusicProgressBarValue;

 }

if (MusicDetails["IsFavourited"] == true) {
    FavouriteImg.src = "static/Icons/Favourite/True.png";
} else {
    FavouriteImg.src = "static/Icons/Favourite/False.png";
}


});



//--------------------------------<Functions>-------------------------------------------

function FormatTime(Seconds){

  if(Seconds < 0){
    return "00:00"
  }

  const TotalSeconds = Math.floor(Math.abs(Seconds));
  
  const Hours = Math.floor(TotalSeconds / 3600);
  const Minutes = Math.floor((TotalSeconds % 3600) / 60);
  const RemainingSeconds = TotalSeconds % 60;

  // Helper function also using PascalCase (or standard camelCase for a local helper)
  const PadNumber = (Num) => String(Num).padStart(2, '0');

  if (Hours > 0) {
    // Format as H:MM:SS
    return `${Hours}:${PadNumber(Minutes)}:${PadNumber(RemainingSeconds)}`;
  } else {
    // Format as MM:SS
    return `${PadNumber(Minutes)}:${PadNumber(RemainingSeconds)}`;
  }
}




function SetDuration(SetTo){
    Socket.emit(
        "ClientSubmit",
        {
            RequestType : "SetDuration",
            Data : SetTo
        }
    )
}


function ClearResultsList(){
document.getElementById("SearchResultsContainer").innerHTML = ""
};

function PlaySong(Url){

    CurrentUrl = Url
    Socket.emit(

        "ClientSubmit",
        {
            RequestType : "PlaySong",
            Data : Url
        }


    )
}


function FavouriteSong(){
    Socket.emit(
        "ClientSubmit",
        {
            RequestType : "SetFavourite",
            Data : CurrentUrl
        }


    )
}

function AddResultsList(Text,Url){ //To do later.
    const ListContainer = document.getElementById("SearchResultsContainer")
    const ListItem = document.createElement("li")
    const ListButton = document.createElement("Button")

    ListItem.style = "list-style-type: none;" //Remove list number.

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
    Data: "PAUSE THAT SH*T"

});
};

function OnSubmit(){

    var MusicInput = document.getElementById("MusicSearch"); // Get all the useful elements.
    ClearResultsList()


    var RequestData = {
        RequestType: "SearchSongs", // Request type
        Data: MusicInput.value // Search
    };


    Socket.emit("ClientSubmit",RequestData)


}


function ShowFavourites(){ // Send server request to show favourites
    Socket.emit(
        "ClientSubmit",
        {RequestType : "ShowFavourites",
         Data: "PLZ PLZ PLZ" // Easter egg

        }

    );
}



