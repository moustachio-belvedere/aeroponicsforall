let temp1 = new XMLHttpRequest();
temp1.open("GET", "sensordata/temp1.json");
temp1.responseType = 'json';
temp1.send();

let temp2 = new XMLHttpRequest();
temp2.open("GET", "sensordata/temp2.json");
temp2.responseType = 'json';
temp2.send();

let datim = new XMLHttpRequest();
datim.open("GET", "sensordata/datim.json");
datim.responseType = 'json';
datim.send();

let plotsentinel = true;

temp1.onload = function () {
  if ((temp1.readyState == 4) && (temp2.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(temp1.response, temp2.response, datim.response);
    plotsentinel = false;
  }
};

temp2.onload = function () {
  if ((temp1.readyState == 4) && (temp2.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(temp1.response, temp2.response, datim.response);
    plotsentinel = false;
  }
};

datim.onload = function () {
  if ((temp1.readyState == 4) && (temp2.readyState == 4) && (datim.readyState == 4) && plotsentinel) {
    ploteverything(temp1.response, temp2.response, datim.response);
    plotsentinel = false;
    }
};

function ploteverything(t1, t2, dt){
  let t1trace = {
    x: dt,
    y: t1,
    name: 'Sensor 1',
    mode: 'lines+markers'
  };

  let t2trace = {
    x: dt,
    y: t2,
    name: 'Sensor 2',
    mode: 'lines+markers'
  };

  let data = [t1trace, t2trace];

  let layout = {
    title: 'Sensor Temperatures',
    xaxis: {
      title: 'Date/Time'
    },
    yaxis: {
      title: 'Temperature (degrees celsius)'
    },
    width: 640,
    height: 480
  };

  Plotly.newPlot('sensorsplot', data, layout);
}


