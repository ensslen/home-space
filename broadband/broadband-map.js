const fetch = require('node-fetch')

const genQuery = (x, y, addr_id) => ({
  query: `https://broadbandmap.nz/api/1.0/networks?x=${x}&y=${y}`,
  addr_id
})

// stub values
// const lat = "174.7931018167"
// const long = "-41.2318559" 

// const getBroadbandInfo = (lat, long, address_id) => {
//   const query = genQuery(lat, long, address_id)
//   console.log(query)
//   return fetch(query)
//     .then(val => val.json())
//     // .then(val => console.log(val))
//     .catch(err => console.error(err))
// }

const fetcher = ({query, addr_id}) =>
  fetch(query)
    .then(resp => resp.json())
    .then(parsed => ({ resp: parsed, addr_id}))

exports.getBroadbandInfoMultiple = latLongs => {
  const queries = latLongs.map(latlong => genQuery(latlong.st_x, latlong.st_y, latlong.address_id))
  console.log("queries: \n", queries)

  return Promise.all(
    queries.map(fetcher))
    .catch(err => console.error(err))
}

// getBroadbandInfo(lat, long)