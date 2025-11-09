import { useState } from 'react'
import './ResultDisplay.css'

function ResultDisplay({ result }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(result.url)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = result.url
    link.download = `timelapse_${result.timestamp}.${result.format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="result-display">
      <div className="result-header">
        <h2>✨ Your Timelapse</h2>
      </div>
      
      <div className="result-content">
        <div className="result-preview">
          {result.format === 'gif' ? (
            <img 
              src={result.url} 
              alt="Generated timelapse" 
              className="timelapse-preview"
            />
          ) : (
            <video 
              src={result.url} 
              controls 
              loop 
              autoPlay 
              muted
              className="timelapse-preview"
            />
          )}
        </div>
        
        <div className="result-info">
          <div className="info-item">
            <span className="info-label">📊 Frames:</span>
            <span className="info-value">{result.frame_count}</span>
          </div>
          <div className="info-item">
            <span className="info-label">📅 Date Range:</span>
            <span className="info-value">{result.date_range}</span>
          </div>
          <div className="info-item">
            <span className="info-label">🎨 Type:</span>
            <span className="info-value">{result.visualization}</span>
          </div>
        </div>
        
        <div className="result-actions">
          <button onClick={handleDownload} className="action-button primary">
            ⬇️ Download
          </button>
          <button onClick={handleCopy} className="action-button secondary">
            {copied ? '✅ Copied!' : '🔗 Copy Link'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ResultDisplay


