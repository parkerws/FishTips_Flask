const temp = document.querySelector('#temp');
const feels = document.querySelector('#feels');
const loc = document.querySelector('#location');
const datetime = document.querySelector('#datetime');
const clouds = document.querySelector('#clouds');
const description = document.querySelector('#description');
const humidity = document.querySelector('#humidity');
const wind = document.querySelector('#wind');
const windDirection = document.querySelector('#windDirection');
const gusts = document.querySelector('#gusts');
const sunrise = document.querySelector('#sunrise');
const sunset = document.querySelector('#sunset');
const weatherImage = document.querySelector('#weatherImage')

const form = document.querySelector("form");
form.addEventListener("submit", e => {
    e.preventDefault();
    console.log(e)
    const location = e.target[0].value;
    console.log(location);
    getWeather(location);
});

const getWeather = location => {
    if (!isNaN(location) && location.length == 5) {
        fetch(`/map/zip_search?location=${location}`).then(res => res.json())
        .then(data => {
            console.log(data);
            let parsedData = JSON.parse(data);
            console.log(parsedData);
            console.log(parsedData.main)
            temp.childNodes[0].nodeValue = parsedData.main.temp;
            feels.childNodes[0].nodeValue = parsedData.main.feels_like;
            loc.textContent = parsedData.name;
            datetime.textContent = moment.unix(parsedData.dt).format('LLLL');
            clouds.textContent = parsedData.clouds.all + '%';
            description.textContent = parsedData.weather[0].description;
            humidity.textContent = parsedData.main.humidity + '%';
            wind.textContent = parsedData.wind.speed + ' mph';
            windDirection.textContent = parsedData.wind.deg;
            gusts.textContent = parsedData.wind.gust + ' mph';
            sunrise.textContent = moment.unix(parsedData.sys.sunrise).format('HH:mm');
            sunset.textContent = moment.unix(parsedData.sys.sunset).format('HH:mm');
            weatherImage.src = `http://openweathermap.org/img/wn/${parsedData.weather[0].icon}@2x.png`;
        });
    } else {
        const encodedLocation = encodeURIComponent(location);
        console.log(encodedLocation);
        fetch(`/map/lat_lng_search?lat=${lat}&lng=${lng}`)
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
    };
};