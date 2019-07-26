let tempT74 = new XMLHttpRequest();
tempT74.open("GET", "sensordata/tempT74.json");
tempT74.responseType = 'json';
tempT74.send();

let tempHON = new XMLHttpRequest();
tempHON.open("GET", "sensordata/tempHON.json");
tempHON.responseType = 'json';
tempHON.send();

let relhHON = new XMLHttpRequest();
relhHON.open("GET", "sensordata/relhHON.json");
relhHON.responseType = 'json';
relhHON.send();

let datim = new XMLHttpRequest();
datim.open("GET", "sensordata/datim.json");
datim.responseType = 'json';
datim.send();

let plotsentinelT = true;
let plotsentinelH = true;

tempT74.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinelT) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinelT = false;
  }
};

tempHON.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinelT) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinelT = false;
  }
};

datim.onload = function () {
  if ((tempT74.readyState == 4) && (tempHON.readyState == 4) && (datim.readyState == 4) && plotsentinelT) {
    ploteverything(tempT74.response, tempHON.response, datim.response);
    plotsentinelT = false;
    };
  if ((relhHON.readyState == 4) && (datim.readyState == 4) && plotsentinelH) {
    plothumidity(relhHON.response, datim.response);
    plotsentinelH = false;
    }    
};

relhHON.onload = function () {
  if ((relhHON.readyState == 4) && (datim.readyState == 4) && plotsentinelH) {
    plothumidity(relhHON.response, datim.response);
    plotsentinelH = false;
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

function plothumidity(h1, dt){
  let t1trace = {
    x: dt,
    y: h1,
    mode: 'lines+markers'
  };

  let data = [t1trace];

  let layout = {
    autosize: false,
    xaxis: {
      title: 'Date/Time'
    },
    yaxis: {
      title: 'Relative Humidity (%)'
    },
    width: 640,
    height: 480,
    margin: {
      l: 40,
      r: 5,
      b: 60,
      t: 20,
      pad: 0
    }
  };

  Plotly.newPlot('humiplot', data, layout);
}



