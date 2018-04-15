window.onload=function(){
  document.getElementById('import').onclick = function() {
    var files = document.getElementById('selectFiles').files;
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

      for(var key in result.goodData) {
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
        //key + "\n" + JSON.stringify(result.goodData[key].bssid) + "\n" + JSON.stringify(result.goodData[key].dtg); 
        var infowindow = new google.maps.InfoWindow();
        var coordSource = JSON.stringify(result.goodData[key].source);
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