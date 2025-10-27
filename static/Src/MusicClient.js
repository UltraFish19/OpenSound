// Music player








function OnSubmit(){

    var MusicInput = document.getElementById("MusicSearch") // Get all the useful elements.


    var Data = {
        RequestType: "SearchSongs", // Request type
        Search: MusicInput.value // Search


    }


    fetch("/SendForm",{
        method: "POST", // Tell it the method
        headers: {
            "Content-Type" : "application/json" // Mention that it is a JSON
        },
        body : JSON.stringify(Data)
    })
    .then(response => response.json)
    .then(ServerData => {
        console.log("Success:", ServerData);
    })
    .catch(Error => {
        console.error("Error:", Error);
    });


}


