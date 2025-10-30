// Music player


const Socket = io();
let SearchingFor = "" // What client is searching for


Socket.on("connect", function(){
console.log("Connected succesfully");
});


Socket.on("GenericResponse",function(Data){ // For responses from the server

console.log("Server Message: " + Data["Status"])

});


Socket.on("SearchResults",function(Data){ // For getting results.



    Result = Data["Result"]
    Details = Data["Details"]



       if (Details["Query"] !== SearchingFor){
        ClearResultsList()
       }

        AddResultsList(Result["Name"] + " by " + Result["Author"], Result["Url"])



});


function ClearResultsList(){
document.getElementById("SearchResultsContainer").innerHTML = ""
}

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



document.addEventListener("keydown",function(Event){ // Press enter to search song
    if (Event.key === "Enter") {
        Event.preventDefault(); // Prevent it from activating when typing and stuff
        OnSubmit();
    }
});


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



