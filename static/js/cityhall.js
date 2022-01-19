function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: { lat: 45.713187, lng: 21.27952 },
  });

  setMarkers(map);
}

const containers = [];


numberOf50 = document.getElementById("nrOf50").innerHTML

for(let i =0;i<numberOf50;i++)
{
  const name = document.getElementById("nameOf50"+i).innerHTML
  const lat = parseFloat(document.getElementById("latOf50"+i).innerHTML)
  const long = parseFloat(document.getElementById("longOf50"+i).innerHTML)
  const sufix = "mm_20_green.png"

  const container = [name,lat,long,sufix]
  containers.push(container)
}


numberOf70 = document.getElementById("nrOf70").innerHTML

for(let i=0;i<numberOf70;i++)
{
  const name = document.getElementById("nameOf70"+i).innerHTML
  const lat = parseFloat(document.getElementById("latOf70"+i).innerHTML)
  const long = parseFloat(document.getElementById("longOf70"+i).innerHTML)
  const sufix = "mm_20_orange.png"

  const container = [name,lat,long,sufix]
  containers.push(container)

}


numberOf100 = document.getElementById("nrOf100").innerHTML

for(let i=0;i<numberOf100;i++)
{
  const name = document.getElementById("nameOf100"+i).innerHTML
  const lat = parseFloat(document.getElementById("latOf100"+i).innerHTML)
  const long = parseFloat(document.getElementById("longOf100"+i).innerHTML)
  const sufix = "mm_20_red.png"

  const container = [name,lat,long,sufix]
  containers.push(container)

}

console.log(containers)
// const containers = [
//     ["punct1", 45.755312, 21.228491, "mm_20_green.png"],
//     ["punct2", 45.713187, 21.27952, "mm_20_brown.png"],
//   ];

function setMarkers(map) {

    const windows = [];

    for (let i = 0; i < containers.length; i++) {
      const container = containers[i];

      const marker = new google.maps.Marker({
        position: { lat: container[1], lng: container[2] },
        map,
        icon: {
          url: "http://labs.google.com/ridefinder/images/" +  container[3]
        },
        title: container[0],
      });
      
      windows.push(marker);
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

        });
    }
}