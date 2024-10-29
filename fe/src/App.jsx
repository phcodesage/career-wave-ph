import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchJobs = async (query) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/jobs`, {
        params: {
          query: query || 'call center' // Default to 'call center' if query is empty
        }
      });
      setJobs(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    fetchJobs(searchQuery);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchJobs(searchQuery);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Job Listings</h1>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search jobs..."
          />
          <button type="submit">Search</button>
        </form>
        
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          <div>
          {jobs.map((job, index) => (
            <div key={index} className="job">
              <div className="job-header">
                <h2>{job.title}</h2>
                <span className={`badge ${job.job_type.toLowerCase().replace(' ', '-')}`}>
                  {job.job_type}
                </span>
              </div>
              <p>{job.description}</p>
              <div className="skills">
                {job.skills.map((skill, i) => (
                  <span key={i} className="skill-badge">{skill}</span>
                ))}
              </div>
              <small>Posted: {job.posted_date}</small>
            </div>
          ))}

          </div>
        )}
      </header>
    </div>
  );
}

export default App;
