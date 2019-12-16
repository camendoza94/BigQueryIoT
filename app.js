// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');

async function queryStackOverflow() {
    // Queries a public Stack Overflow dataset.

    // Create a client
    const bigqueryClient = new BigQuery();

    // The SQL query to run
    const sqlQuery = `SELECT
  location,
  country,
  value,
  latitude,
  longitude,
  EXTRACT(DATETIME FROM timestamp) as time
FROM
  \`bigquery-public-data.openaq.global_air_quality\`
WHERE
  pollutant = "pm10" AND EXTRACT(DATE FROM timestamp) = CURRENT_DATE()
ORDER BY 
  timestamp desc`;

    const options = {
        query: sqlQuery,
        // Location must match that of the dataset(s) referenced in the query.
        location: 'US',
    };

    // Run the query
    const [rows] = await bigqueryClient.query(options);

    console.log('Query Results:');
    rows.forEach(row => {
        const location = row.location;
        const value = row.value;
        const timestamp = new Date(Date.parse(row.time.toString()));
        console.log(row.time);
        console.log(timestamp);
        console.log(`location: ${location}, value: ${value}, timestamp: ${timestamp.toString()}`);
    });
}

queryStackOverflow();