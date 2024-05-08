import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get('http://localhost:5000/jobs');
        setJobs(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Job Listings</h1>
        <div>
          {jobs.map((job, index) => (
            <div key={index} className="job">
              <h2>{job.title}</h2>
              <p>{job.description}</p>
              <small>Posted: {job.posted_date}</small>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
