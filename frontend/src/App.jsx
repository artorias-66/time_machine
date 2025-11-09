import { useState, useEffect } from 'react'
import MapView from './components/MapView'
import ControlPanel from './components/ControlPanel'
import ResultDisplay from './components/ResultDisplay'
import Header from './components/Header'
import './App.css'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [aoi, setAoi] = useState(null)
  const [timelapseResult, setTimelapseResult] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode')
    } else {
      document.body.classList.remove('dark-mode')
    }
  }, [darkMode])

  const handleAOIChange = (newAoi) => {
    setAoi(newAoi)
    setError(null)
  }

  const handleGenerate = async (params) => {
    if (!aoi) {
      setError('Please draw an area of interest on the map')
      return
    }

    setIsGenerating(true)
    setProgress(0)
    setError(null)
    setTimelapseResult(null)

    try {
      const response = await fetch('/api/generate-timelapse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          aoi: aoi,
          start_date: params.startDate,
          end_date: params.endDate,
          cloud_cover: params.cloudCover,
          output_format: params.format,
          add_timestamps: params.addTimestamps,
          visualization: params.visualization,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate timelapse')
      }

      const data = await response.json()
      setTimelapseResult(data)
      setProgress(100)
    } catch (err) {
      setError(err.message)
      console.error('Error generating timelapse:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />
      
      <div className="main-content">
        <div className="map-container">
          <MapView onAOIChange={handleAOIChange} />
        </div>
        
        <div className="sidebar">
          <ControlPanel 
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
            progress={progress}
            error={error}
            aoi={aoi}
          />
          
          {timelapseResult && (
            <ResultDisplay result={timelapseResult} />
          )}
        </div>
      </div>
    </div>
  )
}

export default App


