let div  = document.getElementById("map");
var currentLat = 45.713187;
var currentLong = 21.27952;
var counter = 0;
var windows = [];

function initMap() {
    getLocation(div);
    let containerMap = JsonParser();
    var delayInMilliseconds = 100; //1 second

    setTimeout(function() {
        makeMap(containerMap);
    }, delayInMilliseconds);
}

function makeMap(containerMap) {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: { lat: currentLat, lng: currentLong },
    });

    setMarkers(map, containerMap);
}

function setMarkers(map, containerMap) {


    windows = [];
    let marker = new google.maps.Marker({
            position: { lat: currentLat, lng: currentLong },
            map,
            icon: {
                url: "http://labs.google.com/ridefinder/images/mm_20_blue.png"
            },
            title: "Your location",
            });
        windows.push(marker);
    const latits = [];
    const longs = [];

    for (const cont in containerMap) {
        var simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_green.png";
        if (containerMap[cont][2] === "sticlă")
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_green.png";
        else if (containerMap[cont][2] === "haine")
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_red.png";
        else if (containerMap[cont][2] === "ulei utilizat")
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_orange.png";
        else if (containerMap[cont][2] === "baterii")
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_brown.png";
        else if (containerMap[cont][2] === "deșeuri voluminoase")
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_black.png";
        else
            simple_url = "http://labs.google.com/ridefinder/images/" +  "mm_20_green.png";

        marker = new google.maps.Marker({
            position: { lat: containerMap[cont][1], lng: containerMap[cont][0] },
            map,
            icon: {
                url: simple_url
            },
            title: containerMap[cont][3],
            });
        
        windows.push(marker);
        latits.push(containerMap[cont][1])
        longs.push(containerMap[cont][0])
    }




    for(let i=0;i<windows.length;i++)
      {
          const point = windows[i];

          const infowindow = new google.maps.InfoWindow({
            content: point.title,
          });

          point.addListener("click", () => {

            infowindow.open({
              anchor: point,
              map,
              shouldFocus: false,
            });

            document.getElementById("emptyContainerPres").innerHTML = point.title + " is empty: "
            document.getElementById("emptyContainer").innerHTML = point.title
            document.getElementById("emptyContainerLat").innerHTML = latits[i]
            document.getElementById("emptyContainerLong").innerHTML = longs[i]


          });
      }

}

function calculateDistance( ContainerPosX, ContainerPosY, CurrentPosX1,  CurrentPosY1){
    let a = Math.sqrt((ContainerPosX-CurrentPosX1)*(ContainerPosX-CurrentPosX1) + (ContainerPosY-CurrentPosY1)*(ContainerPosY-CurrentPosY1));
    console.log(a);
    return a;

}

function getLocation(div) {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(FindClosestContainer);
    } else {
        div.innerHTML = "The Browser does not support GeoLocation";
    }
}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

function FindClosestContainer(position) {

    let CurrentPosX = position.coords.latitude;
    let CurrentPosY = position.coords.longitude;

    currentLat = CurrentPosX;
    currentLong = CurrentPosY;

    let containerListOfCoord = JsonParser();

    //----------------------------
    let NameOfContainerAndDistance = [];
    for (const Container in containerListOfCoord) {
        NameOfContainerAndDistance.push({
            key:   Container,
            value: calculateDistance(containerListOfCoord[Container][1] ,  containerListOfCoord[Container][0] , currentLat ,currentLong),
        });
    }

    let newDic = {};
    let min1 = Object.values(NameOfContainerAndDistance[0])[1];
    let min2 = Object.values(NameOfContainerAndDistance[0])[1];
    let min3 = Object.values(NameOfContainerAndDistance[0])[1];
    newDic[Object.values(NameOfContainerAndDistance[0])[0]] = Object.values(NameOfContainerAndDistance[0])[1];
    for (var i=3; i < NameOfContainerAndDistance.length; i++) {
        newDic[Object.values(NameOfContainerAndDistance[i])[0]] = Object.values(NameOfContainerAndDistance[i])[1];
        if (Object.values(NameOfContainerAndDistance[i])[1] < min1) {
            min3 = min2;
            min2 = min1;
            min1 = Object.values(NameOfContainerAndDistance[i])[1];
        } else if (Object.values(NameOfContainerAndDistance[i])[1] < min2) {
            min3 = min2;
            min2 = Object.values(NameOfContainerAndDistance[i])[1];
        } else if (Object.values(NameOfContainerAndDistance[i])[1] < min3) {
            min3 = Object.values(NameOfContainerAndDistance[i])[1];
        }
    }

    console.log(containerListOfCoord[getKeyByValue(newDic , min1)][0]) ; //Name of that container
    console.log(containerListOfCoord[getKeyByValue(newDic , min1)][1]) ;
    console.log(containerListOfCoord[getKeyByValue(newDic , min1)][2]) ;
    console.log(min1);
    document.getElementById("nearest1").innerHTML = containerListOfCoord[getKeyByValue(newDic , min1)][3];
    document.getElementById("nearest2").innerHTML = containerListOfCoord[getKeyByValue(newDic , min2)][3];
    document.getElementById("nearest3").innerHTML = containerListOfCoord[getKeyByValue(newDic , min3)][3];

}

//Here is the Json parser algorithm for aquiring the data for containerListOfCoord
//----------------------------
function JsonParser() {
    let JsonData = json_data.toString()

    JsonData = JsonData.replace('"[', '[');
    JsonData = JsonData.replace(']"', ']');
    let parsedJson = JSON.parse(JsonData);

    let containerList = {
    // ------------Here add the names and coordonates--------------
    };

    counter = 0;
    for(var item in parsedJson){
         let containerTipAndId = parsedJson[item].tip_colectare +'_id'+ parsedJson[item].id;
         let longitudine = parsedJson[item].longitudine;
         let latitudine = parsedJson[item].latitudine;
         let tip = parsedJson[item].tip_colectare;
         let adresa = parsedJson[item].adresa;
         let companie = parsedJson[item].companie;
         let website = parsedJson[item].website;
         containerList[containerTipAndId] = [longitudine, latitudine, tip, adresa, companie, website];
         counter ++;
    }

    return containerList;
}