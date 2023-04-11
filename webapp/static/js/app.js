var predictionId = null;


$( document ).ready(function() {
    if ((window.localStorage.getItem("accessToken") == null) ||
    (window.localStorage.getItem("accessToken") == "undefined")){
        window.location.assign("/");
    }else{
        clearAll();
    }
});


function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        jQuery('#selected-image').attr('src', e.target.result).width(552).height(504);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }


function clearAll(clearInput=true){
    predictionId = null;
    document.getElementById("predicted-label").innerHTML = "N.A.";
    document.getElementById("expected-label").value = "";
    if(clearInput){
        document.getElementById("input-image").value = "";
    }
}

function runClassifier(){
    clearAll(false);

    var form_data = new FormData();
    form_data.append("file", jQuery("#input-image")[0].files[0])
    jQuery.ajax({
        type: 'POST',
        url: '/api/classify',
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data : form_data,
        beforeSend: function (xhr){ 
            document.getElementById("page-loader").style.display = "block";
            xhr.setRequestHeader(
                'Authorization', window.localStorage.getItem("accessToken")
            ); 
        },
        success: function(resultData) { 
            console.log(resultData);
            document.getElementById("predicted-label").innerHTML = resultData["predictedClass"] + " - " + resultData["predictionProbability"] + "%";
            document.getElementById("expected-label").value = resultData["predictedClass"];
            predictionId = resultData["predictionId"];
            
            setTimeout(() => {
                document.getElementById("page-loader").style.display = "none";
            }, 1000);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            alert("Something went wrong");
            setTimeout(() => {
                document.getElementById("page-loader").style.display = "none";
            }, 1000);
            clearAll(false);            
        }
    });

}

function updateLabel(){
    if(predictionId != null) {
        let predictedLabel = document.getElementById("predicted-label").innerHTML;
        let newLabel = document.getElementById("expected-label").value;
        newLabel = newLabel.toLowerCase();

        if ((newLabel != "") && (newLabel != predictedLabel.split("-")[0])){
            jQuery.ajax({
                type: 'POST',
                url: "/api/update-label",
                data: JSON.stringify({
                    predictionId: predictionId,
                    expectedLabel: newLabel
                }),
                beforeSend: function (xhr){ 
                    xhr.setRequestHeader(
                        'Authorization', window.localStorage.getItem("accessToken")
                    ); 
                },
                dataType: "json", 
                contentType: "application/json; charset=utf-8",
                success: function(resultData) { 
                    document.getElementById("predicted-label").innerHTML = "Old: " + predictedLabel + ", New: " +  newLabel;
                    alert("Label Updated Successfully");
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    alert("Something went wrong");
                }
            });
        }
    }
}

function logOut(){
    window.localStorage.removeItem("accessToken");
    window.localStorage.removeItem("refreshToken");
    window.location.assign("/");
}
