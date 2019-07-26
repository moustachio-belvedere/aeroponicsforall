let tempT74 = new XMLHttpRequest();
tempT74.open("GET", "sensordata/tempT74.json");
tempT74.responseType = 'json';
tempT74.send();

let tempHON = new XMLHttpRequest();
tempHON.open("GET", "sensordata/tempHON.json");
tempHON.responseType = 'json';
tempHON.send();

let datim = new XMLHttpRequest();
datim.open("GET", "sensordata/datim.json");
datim.responseType = 'json';
datim.send();

let plotsentinel = true;

tempT74.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinel = false;
  }
};

tempHON.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinel = false;
  }
};

datim.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinel = false;
    }
};

function ploteverything(t1, t2, dt){
  let t1trace = {
    x: dt,
    y: t1,
    name: 'T74',
    mode: 'lines+markers'
  };

  let t2trace = {
    x: dt,
    y: t2,
    name: 'HON',
    mode: 'lines+markers'
  };

  let data = [t1trace, t2trace];

  let layout = {
    autosize: false,
    xaxis: {
      title: 'Date/Time'
    },
    yaxis: {
      title: 'Temperature (degrees celsius)'
    },
    width: 640,
    height: 480,
    margin: {
      l: 40,
      r: 5,
      b: 60,
      t: 20,
      pad: 0
    },
    legend: {
    x: 0.05,
    y: 1
    }
  };

  Plotly.newPlot('sensorsplot', data, layout);
}


