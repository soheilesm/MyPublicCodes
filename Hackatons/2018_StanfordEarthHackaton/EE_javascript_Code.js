//------------------------------------ wind u-velocity ----------------------
var NLDAS = ee.ImageCollection("NASA/NLDAS/FORA0125_H002");

var state = ee.FeatureCollection('ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM')
.filterMetadata('StateName', 'equals', 'California');
Map.addLayer(state);

// Select dates: the Fire data is from 2000-11-01 to 2018-02-27
var quantity1 = NLDAS.filterDate('2013-09-02', '2014-01-01').select('wind_u');
var wind_u = Chart.image.series(quantity1, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
         title: 'U Wind Velocity',
         vAxis: {title: 'm/s'},
});
print(wind_u);

var quantity2 = NLDAS.filterDate('2013-06-02', '2013-09-01').select('wind_u');
var wind_u2 = Chart.image.series(quantity2, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
         title: 'U Wind Velocity',
         vAxis: {title: 'm/s'},
});
print(wind_u2);

var quantity3 = NLDAS.filterDate('2013-03-02', '2013-06-01').select('wind_u');
var wind_u3 = Chart.image.series(quantity3, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
         title: 'U Wind Velocity',
         vAxis: {title: 'm/s'},
});
print(wind_u3);

var quantity4 = NLDAS.filterDate('2013-01-01', '2013-03-01').select('wind_u');
var wind_u4 = Chart.image.series(quantity4, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
         title: 'U Wind Velocity',
         vAxis: {title: 'm/s'},
});
print(wind_u4);

var quantity2 = NLDAS.filterDate('2017-09-01', '2018-01-01').select('wind_v');
var wind_v = Chart.image.series(quantity2, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
        title: 'V Wind Velocity',
        vAxis: {title: 'm/s'},
});
print(wind_v);



var q1 = quantity1.mean().clip(state);

Map.addLayer(q1, {'min': 0, 'max': 100, 'palette':"CCFFCC,00CC66,006600"});

//-------------------------------------- Temp --------------------------------------
// Load the temperature data
var temps = ee.ImageCollection('NCEP_RE/surface_temp')
    .filterDate('2016-01-29', '2016-12-29');

//Identify country/state
var regions = ee.FeatureCollection('ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM')
.filter(ee.Filter.eq('StateName', 'California');

Map.addLayer(regions);

var tempTimeSeries = Chart.image.series(temps, regions, ee.Reducer.max(), 1000,
'system:time_start').setOptions({ title: 'temperature', vAxis: {title: 'temperature'},
}); 

// Display.
print(tempTimeSeries);
    

// Export.table.toDrive({
//   collection: tempTimeSeries,
//   description: 'exportTableExample',
//   fileFormat: 'CSV'
// });

// ------------------------------ Rain -------------------------------------------------
// Load the CHIRPS data
var CHIRPS= ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') 

// Identify country/state
var state = ee.FeatureCollection('ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM')
.filter(ee.Filter.eq('StateName', 'California'));

Map.addLayer(state);

var precip = CHIRPS.filterDate('2013-01-01', '2014-01-01');
var plot = Chart.image.series(precip, state, ee.Reducer.mean(), 10000, 'system:time_start').setOptions({
          title: 'Precipitation Full Time Series', vAxis: {title: 'mm/day'},});
          
print(plot);




// var Precip=precip.mean().clip(state);

// Map.addLayer(Precip, {'min': 0, 'max': 40, 'palette':"CCFFCC,00CC66,006600"});

//------------------------------------- humidity ----------------------------------
// Load the NLDAS data
var NLDAS= ee.ImageCollection('NASA/NLDAS/FORA0125_H002') 

// Identify country/state
var state = ee.FeatureCollection('ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM')
.filterMetadata('StateName', 'equals', 'California');
Map.addLayer(state);

var humid = NLDAS.filterDate('2013-08-02', '2014-01-01').select('specific_humidity');
var plot = Chart.image.series(humid, state, ee.Reducer.mean(), 1000, 'system:time_start').setOptions({
        title: 'Humidity Full Time Series',
        vAxis: {title: 'kg/kg'},
});
print(plot);

var humid2 = NLDAS.filterDate('2013-04-02', '2013-08-01').select('specific_humidity');
var plot2 = Chart.image.series(humid2, state, ee.Reducer.mean(), 1000, 'system:time_start').setOptions({
        title: 'Humidity Full Time Series',
        vAxis: {title: 'kg/kg'},
});
print(plot2);


var humid3 = NLDAS.filterDate('2013-01-01', '2013-04-01').select('specific_humidity');
var plot3 = Chart.image.series(humid3, state, ee.Reducer.mean(), 1000, 'system:time_start').setOptions({
        title: 'Humidity Full Time Series',
        vAxis: {title: 'kg/kg'},
});
print(plot3);

var Humidity = humid.mean().clip(state);
Map.addLayer(Humidity, {'min': 0, 'max': 100, 'palette':"CCFFCC,00CC66,006600"});

// ---------------------------- fire --------------------------------------------

var imageCollection = ee.ImageCollection("FIRMS");
//Add the collection and filter by Date
var firms= ee.ImageCollection('FIRMS')
var filtfirms = firms.filterDate('2013-01-01','2018-01-01')

//There is only one image in the collection now so let's add the first/only one
Map.addLayer(ee.Image(ee.ImageCollection(filtfirms.first())))

var endtime_list = filtfirms.aggregate_array('system:time_end')
var starttime_list = filtfirms.aggregate_array('system:time_start')
var assetsize_list = filtfirms.aggregate_array('system:asset_size')


print(endtime_list)
print(starttime_list)
print(assetsize_list)
print(filtfirms)


// Load a feature collection from a Fusion Table.
var featureCollection = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');

// Filter the collection.
var filteredFC = featureCollection.filter(ee.Filter.eq('Name', 'California'));

Display the collection.
Map.addLayer(filteredFC, {}, 'California');
      

var TS1 = Chart.image.series(firms, firms.first(),  ee.Reducer.mean(),1000, 'system:time_start').setOptions({
         title: 'Precipitation 1-Year Time Series',
         vAxis: {title: 'mm/pentad'},
});

//Set a lat long and zoom level for the setup
Map.setCenter(-118.3179, 34.218,11)

//To make it look slightly better set the background to be Satellite imagery instead of Map
Map.setOptions('SATELLITE')
