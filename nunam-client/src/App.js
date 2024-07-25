import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';


function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/')
      .then(response => response.json())
      .then(json => setData(json));
      console.log(data)
  }, []);

  return (
    <div>
      <div style={{backgroundColor: "black", color: "white"}}>
        <h1 style={{textAlign: "center", margin:0, padding: "15px"}}>Nunam Dashboard Assignment</h1>
      </div>
      {data ? 
      <div style={{display:'flex', flexDirection:"column", justifyItems: "center", margin:"25px"}}>
        <Plot data={JSON.parse(data.chart1).data} layout={JSON.parse(data.chart1).layout} />
        <Plot data={JSON.parse(data.chart2).data} layout={JSON.parse(data.chart2).layout} />
        <Plot data={JSON.parse(data.chart3).data} layout={JSON.parse(data.chart3).layout} />
        <Plot data={JSON.parse(data.chart4).data} layout={JSON.parse(data.chart4).layout} />
      </div> : <p>Loading...</p>}
    </div>
  );
}
export default App;
