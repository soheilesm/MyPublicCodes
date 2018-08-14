// Define a FeatureCollection: regions of the American West.
var regions = ee.FeatureCollection([
 ee.Feature(    // San Francisco.
   ee.Geometry.Rectangle(-122.45, 37.74, -122.4, 37.8), {label: 'City'}),
 ee.Feature(  // Tahoe National Forest.
   ee.Geometry.Rectangle(-121, 39.4, -120.8, 39.8), {label: 'Forest'}),
 ee.Feature(  // Black Rock Desert.
   ee.Geometry.Rectangle(-119.15, 40.8, -119, 41), {label: 'Desert'})
]);

// Load Landsat 8 brightness temperature data for 1 year.
var temps2013 = ee.ImageCollection('LANDSAT/LC8_L1T_32DAY_TOA')
   .filterDate('2012-12-25', '2013-12-25')
   .select('B11');

// Collect region, image, value triplets.
var triplets = temps2013.map(function(image) {
 return image.select('B11').reduceRegions({
   collection: regions.select(['label']), 
   reducer: ee.Reducer.mean(), 
   scale: 30
 }).filter(ee.Filter.neq('mean', null))
   .map(function(f) { 
     return f.set('imageId', image.id());
   });
}).flatten();
print(triplets.first());

// Format a table of triplets into a 2D table of rowId x colId.
var format = function(table, rowId, colId) {
 // Get a FeatureCollection with unique row IDs.
 var rows = table.distinct(rowId);
 // Join the table to the unique IDs to get a collection in which
 // each feature stores a list of all features having a common row ID. 
 var joined = ee.Join.saveAll('matches').apply({
   primary: rows, 
   secondary: table, 
   condition: ee.Filter.equals({
     leftField: rowId, 
     rightField: rowId
   })
 });

 return joined.map(function(row) {
     // Get the list of all features with a unique row ID.
     var values = ee.List(row.get('matches'))
       // Map a function over the list of rows to return a list of
       // column ID and value.
       .map(function(feature) {
         feature = ee.Feature(feature);
         return [feature.get(colId), feature.get('mean')];
       });
     // Return the row with its ID property and properties for
     // all matching columns IDs storing the output of the reducer.
     // The Dictionary constructor is using a list of key, value pairs.
     return row.select([rowId]).set(ee.Dictionary(values.flatten()));
   });
};

var link = '6430802a354ca3e5d5267718173afac7';

var table1 = format(triplets, 'imageId', 'label');

var desc1 = 'table_demo_' + link; 
Export.table.toDrive({
 collection: table1, 
 description: desc1, 
 fileNamePrefix: desc1,
 fileFormat: 'CSV'
});
