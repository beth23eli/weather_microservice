import React, { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";


const WeatherChartComponent = () => {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/weather-data")
      .then(res => res.json())
      .then(data => {
        setSeries(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading data:", err);
        setLoading(false);
      });
  }, []);

  const options = {
    chart: {
      type: "line",
      height: 350,
      zoom: { enabled: false },
      toolbar: { show: false }
    },
    stroke: {
      curve: "smooth"
    },
    title: {
      text: "Temperature Chart",
      align: "left"
    },
    xaxis: {
      type: "datetime",
      title: { text: "Date" },
      labels: { rotate: -45 }
    },
    yaxis: {
      title: { text: "Temperature (°C)" },
      min: 0,
      max: 40
    },
    tooltip: {
      shared: true,
      intersect: false
    },
    legend: {
      position: "top",
      horizontalAlign: "right"
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
    <div>
      <ReactApexChart
        options={options}
        series={series}
        type="line"
        height={350}
      />
    </div>
  );
};

export default WeatherChartComponent;
