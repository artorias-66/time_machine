import { useState } from 'react'
import './ControlPanel.css'

function ControlPanel({ onGenerate, isGenerating, progress, error, aoi }) {
  const [startDate, setStartDate] = useState('2023-01-01')
  const [endDate, setEndDate] = useState('2023-06-01')
  const [cloudCover, setCloudCover] = useState(30)
  const [format, setFormat] = useState('gif')
  const [addTimestamps, setAddTimestamps] = useState(true)
  const [visualization, setVisualization] = useState('true-color')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!aoi) {
      return
    }
    
    onGenerate({
      startDate,
      endDate,
      cloudCover,
      format,
      addTimestamps,
      visualization,
    })
  }

  return (
    <div className="control-panel">
      <div className="panel-header">
        <h2>⚙️ Settings</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="control-form">
        <div className="form-group">
          <label htmlFor="start-date">
            📅 Start Date
          </label>
          <input
            id="start-date"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            max={endDate}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="end-date">
            📅 End Date
          </label>
          <input
            id="end-date"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            min={startDate}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="cloud-cover">
            ☁️ Max Cloud Cover: {cloudCover}%
          </label>
          <input
            id="cloud-cover"
            type="range"
            min="0"
            max="100"
            value={cloudCover}
            onChange={(e) => setCloudCover(parseInt(e.target.value))}
          />
          <div className="range-labels">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="visualization">
            🎨 Visualization
          </label>
          <select
            id="visualization"
            value={visualization}
            onChange={(e) => setVisualization(e.target.value)}
          >
            <option value="true-color">True Color (RGB)</option>
            <option value="false-color">False Color (NIR)</option>
            <option value="ndvi">NDVI (Vegetation)</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="format">
            🎞️ Output Format
          </label>
          <select
            id="format"
            value={format}
            onChange={(e) => setFormat(e.target.value)}
          >
            <option value="gif">GIF (Animated)</option>
            <option value="mp4">MP4 (Video)</option>
          </select>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={addTimestamps}
              onChange={(e) => setAddTimestamps(e.target.checked)}
            />
            <span>Add timestamps to frames</span>
          </label>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {!aoi && (
          <div className="info-message">
            ℹ️ Please draw an area on the map first
          </div>
        )}

        <button 
          type="submit" 
          className="generate-button"
          disabled={isGenerating || !aoi}
        >
          {isGenerating ? '⏳ Generating...' : '🚀 Generate Timelapse'}
        </button>

        {isGenerating && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="progress-text">
              Processing satellite imagery... {progress}%
            </p>
          </div>
        )}
      </form>
    </div>
  )
}

export default ControlPanel


