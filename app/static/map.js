
let myMap = L.map('mapid').setView([34.552769, -77.397209], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  
}).addTo(myMap);

L.control.scale().addTo(myMap)

const stations = fetch('/map').then(res => res.json()).then(data => {
    data.forEach(station =>
        L.marker([station['lat'], station['long']]).bindPopup(`Station ID: ${station['station_id']} \nLat: ${station['lat']} Long: ${station['long']} <canvas style="width:30vh; height:25vh;" id="${station['station_id']}"></canvas>`, {closeOnClick:true,autoClose:true,maxWidth: 560} )
        .on('popupopen', fetchTides)
        .addTo(myMap));
        
}).catch(err => alert(err + 'Unable to fetch stations. Refresh the page to retry.'));

const addChartData = (chart, label, data) => {
    chart.data.datasets.push({'data': data});
    chart.options.scales.xAxes[0].time.min = label[0];
    chart.options.scales.xAxes[0].time.max = label.slice(-1)[0];
    chart.update();
};

const removeChartData = (chart) => {
    chart.data.datasets.pop();
    chart.update();
};

const fetchTides = (event) => {
    console.log(event);
    var ctx = event.target._popup._contentNode.lastChild;
    console.log(ctx);
    let chart = new Chart(ctx, {
        
        type: 'line',
        data: {
            datasets: [{
                data: [{
                    t: "2020-12-18T03:45",
                    y: -0.5
                },
                {
                    t: "2020-12-18T08:15",
                    y: 1.2
                },
                {
                    t: "2020-12-18T13:55",
                    y: -0.3
                },
                {
                    t: "2020-12-18T20:45",
                    y: 1.8
                }    
            ]
            }]
        },
        options: {
            legend : {
                display: false
            },
            scales: {
                xAxes: [{
                    scaleLabel : {
                        display: true,
                        labelString: 'Time of Day'
                    },
                    type: 'time',
                    time: {
                        unit: 'hour',
                        unitStepSize: 4,
                        min: moment().startOf('day').format(),
                        max: moment().endOf('day').format(),
                        tooltipFormat: 'HH:mm',
                        displayFormats: {
                            hour: 'HH:mm'
                        }

                    },
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }
                ],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Height in Feet'
                    }
                }]}
        }
    
    });
    const [labels, tides] = [[], []];
    
    let id = event.target._popup._contentNode.lastChild.attributes[1].nodeValue;
    fetch(`https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=${id}&product=predictions&datum=MTL&time_zone=lst&interval=hilo&units=english&format=json`)
        .then(res => res.json())
        .then(data => {
            data['predictions'].forEach(tide => {
            labels.push(tide['t']);
            tides.push({'t': moment(tide['t']).format(), 'y':tide['v']});
            });
            removeChartData(chart);
            addChartData(chart, labels, tides);
        }).catch((error) => console.error(error + ": cannot fetch tides"));


    
    
    //console.log(tideData)
    //console.log(popup.getContent().split(' ')[2])
};

const getCurrentLocation = (e) => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert('Geolocation not available');
    }
};

const showPosition = position => {
    alert(`Latitude: ${position.coords.latitude} Longitude:  ${position.coords.longitude}`);
};

const getLocation = (e) => {
    let address = document.querySelector('#address').value;
    console.log(address);
    const location = encodeURIComponent(address);
    console.log(location);
    const response = fetch(`/map/convert_location/${location}`).then(res => res.json()).then(data => {
        let parsedData = JSON.parse(data);
        console.log(parsedData.results[0].geometry.location);
        myMap.setView(parsedData.results[0].geometry.location, 10);

    });
};

//let address = document.querySelector('#address').value
const addressFinder = document.querySelector('#addressFinder');
addressFinder.addEventListener('click', getLocation);
//const locator = document.querySelector('#locator');
//locator.addEventListener('click', getCurrentLocation);

