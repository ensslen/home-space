const pgp = require('pg-promise')(),
  QueryFile = require('pg-promise').QueryFile,
  path = require('path'),
  fs = require('fs'),
  R = require('ramda'),
  papa = require('papaparse'),
  broadband = require('./broadband-map.js'),
  // get the lat/long values of every trademe listing
  get_lat_long = new QueryFile(path.join(__dirname, 'get-lat-long.sql')),
  output_file = path.join(__dirname, 'broadband.csv')

const connection = {
  host: 'govhackdb.co2bawa2k0lu.ap-southeast-2.rds.amazonaws.com',
  port: 5432,
  database: 'govhack',
  user: 'lewis',
  password: process.argv[2]
}

const db = pgp(connection)

const parseToCSV = vals => papa.unparse(vals)

const onlyAvailable = vals =>
  vals.map(x => {
    x.resp.results = x.resp.results.filter(result => result.availability == "Available")
    return x;
  })

const getSpeed = house =>
  house.results.map(res => res.providers.map(R.prop('bandwidth_max_mbps')))[0]

const maxSpeed = house => getSpeed(house).reduce(R.max)

const flattenParse = vals =>
  vals.map(house => ({
    address_id: house.addr_id,
    technology: "{" + house.resp.results.map(R.prop('technology')) + "}",
    providers: "{" + house.resp.results.map(res => res.providers.map(R.prop('name'))) + "}",
    top_speed: maxSpeed(house.resp)
  }))

const writeCSV = csv =>
  fs.writeFile(output_file, csv, err => {
      if(err) {
          return console.log(err);
      }

      console.log("The file was saved!");
  }); 

db.query(get_lat_long)
  .then(broadband.getBroadbandInfoMultiple)
  // .then(vals => {
  //   console.log(vals.resp)
  //   return vals
  // })
  .then(onlyAvailable)
  // .then(vals => {
  //   console.log(vals)
  //   return vals
  // })
  .then(flattenParse)
  .then(parseToCSV)
  // .then(csvs => console.log(csvs))
  .then(writeCSV)
  .catch(err => console.error(err))
    