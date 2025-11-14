import './DummyDataModal.css'

function DummyDataModal({ open, onClose, dataSource }) {
  if (!open) return null

  const isDummy = dataSource !== 'arlula'

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="dummy-modal-title">
      <div className="modal">
        <div className="modal-header">
          <h3 id="dummy-modal-title">{isDummy ? 'Demo Imagery In Use' : 'Live Imagery In Use'}</h3>
        </div>
        <div className="modal-body">
          {isDummy ? (
            <>
              <p>
                Your timelapse was generated using demo (synthetic) imagery because satellite API credentials
                were not available or the provider returned no results for this area/date range.
              </p>
              <ul>
                <li>The images may not match the selected geographic area.</li>
                <li>Visualization and timestamps still reflect your settings.</li>
              </ul>
              <p className="tip">
                Add valid API keys (e.g., Arlula) in the backend environment to enable real satellite imagery.
              </p>
            </>
          ) : (
            <p>Real satellite thumbnails were used to generate this timelapse.</p>
          )}
        </div>
        <div className="modal-footer">
          <button className="btn" onClick={onClose} autoFocus>Got it</button>
        </div>
      </div>
    </div>
  )
}

export default DummyDataModal
