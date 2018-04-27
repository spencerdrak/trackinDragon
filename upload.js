// Works Cited: I adapted the following code from various examples in the Google Maps API: https://developers.google.com/maps/documentation/javascript/tutorial
// I borrowed from this example on how to use the Maps API: https://developers.google.com/maps/documentation/javascript/examples/event-closure
window.onload=function(){
  document.getElementById('import').onclick = function() {
    //I adapted the answer from Maloric on the following Stackoverflow answer to help upload the JSON to the page: https://stackoverflow.com/questions/36127648/uploading-a-json-file-and-using-it
    var files = document.getElementById('selectFiles').files;
    //I used Kasun's answer on stack overflow to write this line: https://stackoverflow.com/questions/6756104/get-size-of-json-object
    if (files.length <= 0) {
      return false;
    }
    
    var fr = new FileReader();
    
    fr.onload = function(e) { 
      result = JSON.parse(e.target.result);

      var analysisTime = result["analysisTime"]
      var registryFile = result["registryFile"]

      alert("You've uploaded " + registryFile + " which was gathered at " + analysisTime);

      var compCoordinates = [];

      //Works Cited: I used "Your Friend Ken"'s answer on Stackoverflow to iterate over the line: https://stackoverflow.com/questions/1078118/how-do-i-iterate-over-a-json-structure. 
      for(var key in result.goodData) {
        //Works Cited: I used Tamil Selvan C's answer to work out how the stringify method worked: https://stackoverflow.com/questions/16493498/json-stringify-returns-object-object-instead-of-the-contents-of-the-object
        var latitude = JSON.stringify(result.goodData[key].coords.lat);
        var longitude = JSON.stringify(result.goodData[key].coords.lng);
        var c = new google.maps.LatLng(latitude,longitude);
        compCoordinates.push(c);
        
        var content = '<div id="content">'+
        '<div id="siteNotice">'+
        '</div>'+
        '<h1 id="firstHeading" class="firstHeading">'+key+'</h1>'+
        '<div id="bodyContent">'+
        '<p> BSSID: ' + JSON.stringify(result.goodData[key].bssid) + "\n" + '</p>'+
        '<p> First Connection Time: ' + JSON.stringify(result.goodData[key].dtg) + '</p>'+
        '</div>'+
        '</div>';
        var infowindow = new google.maps.InfoWindow();
        var coordSource = JSON.stringify(result.goodData[key].source);
        //I used Matt Burns answer for how to differently color the icons: https://stackoverflow.com/questions/7095574/google-maps-api-3-custom-marker-color-for- default-dot-marker/7686977#7686977
        if(coordSource == "1"){
          var marker = new google.maps.Marker({
            position: c,
            map: map,
            title: key,
            icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
          });
        }
        else{
          var marker = new google.maps.Marker({
            position: c,
            map: map,
            title: key,
            icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
          });
        }
        markers.push(marker);
        //Works Cited: I used Engineer's stackoverflow answer to ensure each dot had it's own text: https://stackoverflow.com/questions/11106671/google-maps-api-multiple-markers-with-infowindows
        google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
          return function() {
              infowindow.setContent(content);
              infowindow.open(map,marker);
          };
        })(marker,content,infowindow));
      }

      compPath = new google.maps.Polyline({
        path: compCoordinates,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      for(var key in result.badData) {
        s = key + " " + JSON.stringify(result.badData[key].bssid) + " " +JSON.stringify(result.badData[key].dtg) + "<br>";
        document.getElementById('unfound').innerHTML += s;
      }

      compPath.setMap(map);

    }
    fr.readAsText(files.item(0));
  };
}