var predictionId = null;


function clearAll(clearInput=true){
    predictionId = null;
    document.getElementById("predicted-label").innerHTML = "N.A.";
    document.getElementById("expected-label").value = "";
    if(clearInput){
        document.getElementById("input-image").value = "";
    }
}

function runClassifier(){
    document.getElementById("page-loader").style.display = "block";
    clearAll(false);

    var form_data = new FormData();
    form_data.append("file", jQuery("#input-image")[0].files[0])
    $.ajax({
        type: 'POST',
        url: '/api/classify',
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data : form_data,
        success: function(resultData) { 
            console.log(resultData);
            document.getElementById("page-loader").style.display = "none";
            document.getElementById("predicted-label").innerHTML = resultData["predictedClass"];
            document.getElementById("expected-label").value = resultData["predictedClass"];
            predictionId = resultData["predictionId"];
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            alert("Something went wrong");
            document.getElementById("page-loader").style.display = "none";
            clearAll(false);            
        }
    });

}

function updateLabel(){
    if(predictionId != null) {
        let predictedLabel = document.getElementById("predicted-label").innerHTML;
        let newLabel = document.getElementById("expected-label").value;
        newLabel = newLabel.toLowerCase();

        if ((newLabel != "") && (newLabel != predictedLabel)){
            jQuery.ajax({
                type: 'POST',
                url: "/api/update-label",
                data: JSON.stringify({
                    predictionId: predictionId,
                    expectedLabel: newLabel
                }),
                dataType: "json", 
                contentType: "application/json; charset=utf-8",
                success: function(resultData) { 
                    document.getElementById("predicted-label").innerHTML = newLabel;
                    alert("Label Updated Successfully");
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    alert("Something went wrong");
                }
            });
        }
    }
}
