import './Header.css'

function Header({ darkMode, setDarkMode }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="header-title">
            🌍 Time Machine for Earth
          </h1>
          <p className="header-subtitle">
            Visualize Earth's changes through satellite imagery
          </p>
        </div>
        
        <button 
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
          aria-label="Toggle dark mode"
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </header>
  )
}

export default Header


