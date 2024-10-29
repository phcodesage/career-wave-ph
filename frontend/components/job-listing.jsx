'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, Briefcase, MapPin, Calendar, ArrowLeft } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function JobListingJsx() {
  const [jobs, setJobs] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedJob, setSelectedJob] = useState(null)
  const getJobTypeBadgeVariant = (jobType) => {
    const type = jobType?.toLowerCase() || ''
    if (type.includes('full')) return 'bg-emerald-500 text-white'
    if (type.includes('part')) return 'bg-amber-500 text-white'
    if (type.includes('gig')) return 'bg-purple-500 text-white'
    if (type.includes('any')) return 'bg-blue-500 text-white'
    return 'bg-gray-500 text-white'
  }
  
  const fetchJobs = async (query) => {
    setIsLoading(true)
    try {
      const response = await axios.get(`http://localhost:5000/jobs`, {
        params: { query }
      })
      setJobs(response.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    const initialFetch = async () => {
      await fetchJobs('')
    }
    initialFetch()
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    fetchJobs(searchQuery)
    setSelectedJob(null)
  }

  const handleJobClick = (job) => {
    setSelectedJob(job)
  }

  const handleBack = () => {
    setSelectedJob(null)
  }

  return (
    <div className="min-h-screen bg-[#f8fafc] text-[#1e293b] font-sans p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">Job Listings</h1>
        
        <Card className="mb-8">
          <CardContent>
            <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 items-end">
              <div className="flex-1">
                <Input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search jobs..."
                  className="w-full"
                />
              </div>
              <Button type="submit" className="w-full md:w-auto">
                <Search className="mr-2 h-4 w-4" /> Search
              </Button>
            </form>
          </CardContent>
        </Card>
        
        {isLoading ? (
          <div className="text-center">Loading...</div>
        ) : selectedJob ? (
          <Card>
            <CardHeader>
              <Button variant="ghost" onClick={handleBack} className="mb-4">
                <ArrowLeft className="mr-2 h-4 w-4" /> Back to listings
              </Button>
              <CardTitle>{selectedJob.title}</CardTitle>
              <CardDescription>{selectedJob.company}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4 mb-4">
                <Badge variant="secondary">
                  <Briefcase className="mr-2 h-4 w-4" />
                  {selectedJob.job_type}
                </Badge>
                <Badge variant="secondary">
                  <MapPin className="mr-2 h-4 w-4" />
                  {selectedJob.location}
                </Badge>
                <Badge variant="secondary">
                  <Calendar className="mr-2 h-4 w-4" />
                  Posted: {selectedJob.posted_date}
                </Badge>
              </div>
              <p className="mb-4">{selectedJob.description}</p>
              <div className="flex flex-wrap gap-2">
                {selectedJob.skills?.map((skill, index) => (
                  <Badge key={`skill-${index}`} variant="outline">{skill}</Badge>
                ))}
              </div>
            </CardContent>
            <CardFooter>
              <Button asChild className="w-full">
                <a href={selectedJob.url} target="_blank" rel="noopener noreferrer">
                  Apply Now
                </a>
              </Button>
            </CardFooter>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map((job, index) => (
              <Card 
                key={`job-${index}-${job.title}`} 
                className="cursor-pointer hover:shadow-md transition-shadow"
              >
                <CardHeader>
                  <CardTitle>{job.title}</CardTitle>
                  <CardDescription>{job.company}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2 mb-4">
                    <Badge variant="secondary">
                      <Briefcase className="mr-2 h-4 w-4" />
                      {job.job_type}
                    </Badge>
                    <Badge variant="secondary">
                      <MapPin className="mr-2 h-4 w-4" />
                      {job.location}
                    </Badge>
                  </div>
                  <p className="text-sm line-clamp-3">{job.description}</p>
                </CardContent>
                <CardFooter>
                  <Button 
                    variant="outline" 
                    className="w-full" 
                    onClick={() => handleJobClick(job)}
                  >
                    View Details
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
